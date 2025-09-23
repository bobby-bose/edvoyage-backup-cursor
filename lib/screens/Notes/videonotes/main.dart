import 'dart:convert';
import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;
import 'package:frontend/screens/notes/constants.dart';
import 'package:frontend/screens/notes/logo.dart';
import 'package:frontend/screens/notes/topbar.dart';
import 'package:frontend/screens/notes/videonotes/sub.dart'; // VideoTopicsScreen
import 'package:frontend/utils/colors/colors.dart';
import 'package:frontend/utils/responsive.dart';

// Data model for a Subject
class Subject {
  final int id;
  final String name;
  final int videoCount;

  Subject({required this.id, required this.name, required this.videoCount});

  factory Subject.fromJson(Map<String, dynamic> json) {
    return Subject(
      id: json['subject'] is int
          ? json['subject']
          : int.tryParse(json['subject']?.toString() ?? '0') ?? 0,
      name: json['subject_name']?.toString() ?? 'Unknown',
      videoCount: (json['video_count'] is int)
          ? json['video_count']
          : int.tryParse(json['video_count']?.toString() ?? '0') ?? 0,
    );
  }
}

class VideoSubjectScreen extends StatefulWidget {
  const VideoSubjectScreen({super.key});

  @override
  State<VideoSubjectScreen> createState() => _VideoSubjectScreenState();
}

class _VideoSubjectScreenState extends State<VideoSubjectScreen> {
  Measurements? size;
  bool isLoading = true;
  List<Subject> subjects = []; // Correct type: List<Subject>

  @override
  void initState() {
    super.initState();
    fetchSubjects();
  }

  Future<void> fetchSubjects() async {
    setState(() {
      isLoading = true;
    });

    try {
      final response = await http.get(Uri.parse("${API}videos/"));

      if (response.statusCode == 200) {
        final decoded = jsonDecode(response.body);

        // Determine where the list is: in decoded['results'] or decoded itself
        List<dynamic> dataList;
        if (decoded is Map<String, dynamic> &&
            decoded.containsKey('results') &&
            decoded['results'] is List) {
          dataList = decoded['results'] as List<dynamic>;
        } else if (decoded is List) {
          dataList = decoded;
        } else {
          // Unexpected structure
          throw Exception('Unexpected response structure when fetching videos');
        }

        // Group by subject_name and count the videos
        final Map<String, List<dynamic>> subjectsMap = {};
        for (var item in dataList) {
          if (item is Map<String, dynamic>) {
            final subjectName = (item['subject_name'] ?? 'Unknown').toString();
            subjectsMap.putIfAbsent(subjectName, () => []);
            subjectsMap[subjectName]!.add(item);
          }
        }

        final List<Subject> tempSubjects = subjectsMap.entries.map((entry) {
          final subjectName = entry.key;
          final videoList = entry.value;
          // get subject id from the first item that's an int or convertible
          int subjectId = 0;
          for (var v in videoList) {
            if (v is Map<String, dynamic> && v.containsKey('subject')) {
              final raw = v['subject'];
              if (raw is int) {
                subjectId = raw;
                break;
              } else if (raw != null) {
                subjectId = int.tryParse(raw.toString()) ?? 0;
                if (subjectId != 0) break;
              }
            }
          }

          return Subject(
            id: subjectId,
            name: subjectName,
            videoCount: videoList.length,
          );
        }).toList();

        setState(() {
          subjects = tempSubjects;
          isLoading = false;
        });
      } else {
        // non-200
        debugPrint(
            'fetchSubjects: HTTP ${response.statusCode} - ${response.body}');
        setState(() {
          isLoading = false;
        });
        throw Exception(
            'Failed to load subjects (status ${response.statusCode})');
      }
    } catch (e, st) {
      debugPrint("Error fetching subjects: $e\n$st");
      setState(() {
        isLoading = false;
      });
    }
  }

  Widget buildSubjectCard(Subject subject) {
    return GestureDetector(
      onTap: () {
        Navigator.push(
          context,
          MaterialPageRoute(
            builder: (context) =>
                VideosBySubjectScreen(subjectName: subject.name),
          ),
        );
      },
      child: Card(
        elevation: 2,
        clipBehavior: Clip.antiAlias,
        shape: RoundedRectangleBorder(
          borderRadius: BorderRadius.circular(16.0),
        ),
        margin: const EdgeInsets.symmetric(vertical: 10, horizontal: 16),
        child: SizedBox(
          height: 200,
          width: double.infinity,
          child: Column(
            children: [
              ListTile(
                title: Text(
                  subject.name,
                  style: const TextStyle(
                    fontSize: 22,
                    fontWeight: FontWeight.bold,
                  ),
                ),
                trailing: const Icon(Icons.more_vert),
              ),
              const Expanded(child: SizedBox()),
              Padding(
                padding: const EdgeInsets.symmetric(horizontal: 16.0),
                child: Align(
                  alignment: Alignment.centerRight,
                  child: Container(
                    padding: const EdgeInsets.symmetric(
                      horizontal: 12,
                      vertical: 4,
                    ),
                    decoration: BoxDecoration(
                      color: Colors.grey[200],
                      borderRadius: BorderRadius.circular(12),
                    ),
                    child: Text(
                      '${subject.videoCount} Modules',
                      style: TextStyle(
                        color: primaryColor,
                        fontWeight: FontWeight.w800,
                        fontSize: 20,
                      ),
                    ),
                  ),
                ),
              ),
              const SizedBox(height: 16),
              Container(
                height: 20,
                width: double.infinity,
                color: primaryColor,
              ),
            ],
          ),
        ),
      ),
    );
  }

  @override
  Widget build(BuildContext context) {
    size = Measurements(MediaQuery.of(context).size);

    return Scaffold(
      appBar: CustomLogoAppBar(),
      body: Column(
        children: [
          // ADDED: Your Topbar widget
          Topbar(firstText: "Video", secondText: ""),
          // ADDED: Expanded widget to properly size the ListView
          Expanded(
            child: isLoading
                ? const Center(child: CircularProgressIndicator())
                : ListView.builder(
                    padding: const EdgeInsets.only(top: 10),
                    itemCount: subjects.length,
                    itemBuilder: (context, index) {
                      return buildSubjectCard(subjects[index]);
                    },
                  ),
          ),
        ],
      ),
    );
  }
}
