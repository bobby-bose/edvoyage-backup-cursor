import 'dart:convert';
import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;
import 'package:notes/screens/constants.dart';
import 'package:notes/screens/logo.dart';
import 'package:notes/screens/topbar.dart';
import 'package:notes/screens/videonotes/sub.dart'; // VideoTopicsScreen
import 'package:notes/utils/colors/colors.dart';
import 'package:notes/utils/responsive.dart';

// Data model for a Subject
class Subject {
  final int id;
  final String name;
  final int videoCount;

  Subject({required this.id, required this.name, required this.videoCount});

  factory Subject.fromJson(Map<String, dynamic> json) {
    // This factory is no longer used for the top-level Subject list,
    // but is kept for future use if needed.
    return Subject(
      id: json['id'],
      name: json['name'],
      videoCount: json['video_count'],
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
    try {
      final response = await http.get(Uri.parse("${API}videos/"));

      if (response.statusCode == 200) {
        final List<dynamic> data = jsonDecode(response.body);

        // Group the data by subject_name and count the videos
        final Map<String, List<dynamic>> subjectsMap = {};
        for (var item in data) {
          final subjectName = item['subject_name'] as String;
          if (!subjectsMap.containsKey(subjectName)) {
            subjectsMap[subjectName] = [];
          }
          subjectsMap[subjectName]!.add(item);
        }

        // Create a new list of Subject objects from the grouped data
        final List<Subject> tempSubjects = subjectsMap.entries.map((entry) {
          final subjectName = entry.key;
          final videoList = entry.value;

          return Subject(
            id: videoList.first['subject'], // Use the first item's subject ID
            name: subjectName,
            videoCount: videoList.length,
          );
        }).toList();

        setState(() {
          subjects = tempSubjects;
          isLoading = false;
        });
      } else {
        throw Exception('Failed to load subjects');
      }
    } catch (e) {
      setState(() {
        isLoading = false;
      });
      debugPrint("Error fetching subjects: $e");
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
