import 'dart:convert';
import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;
import 'package:notes/screens/constants.dart';
import 'package:notes/screens/logo.dart';
import 'package:notes/screens/topbar.dart';

// Make sure to create this new file and widget as shown in the next step
import 'sub.dart';

class McqSubject {
  final String subjectName;
  final int moduleCount;

  McqSubject({required this.subjectName, required this.moduleCount});

  factory McqSubject.fromJson(Map<String, dynamic> json) {
    return McqSubject(
      subjectName: json['subject']?['name'] ?? 'Unknown',
      moduleCount: 1, // default, will be aggregated later
    );
  }

  @override
  String toString() =>
      "McqSubject(subjectName: $subjectName, modules: $moduleCount)";
}

class McqSubjectsScreen extends StatefulWidget {
  const McqSubjectsScreen({super.key});

  @override
  State<McqSubjectsScreen> createState() => _McqSubjectsScreenState();
}

class _McqSubjectsScreenState extends State<McqSubjectsScreen> {
  bool isLoading = true;
  List<McqSubject> mcqSubjects = [];

  @override
  void initState() {
    super.initState();
    fetchMcqSubjects();
  }

  Future<void> fetchMcqSubjects() async {
    try {
      final response = await http.get(Uri.parse("${API}mcqs/"));

      if (response.statusCode == 200) {
        final List<dynamic> data = jsonDecode(response.body);

        List<McqSubject> allSubjects = data
            .map((json) => McqSubject.fromJson(json))
            .toList();

        Map<String, int> subjectCounts = {};
        for (var subject in allSubjects) {
          subjectCounts[subject.subjectName] =
              (subjectCounts[subject.subjectName] ?? 0) + 1;
        }

        List<McqSubject> uniqueSubjects = subjectCounts.entries
            .map(
              (entry) =>
                  McqSubject(subjectName: entry.key, moduleCount: entry.value),
            )
            .toList();

        setState(() {
          mcqSubjects = uniqueSubjects;
          isLoading = false;
        });

        debugPrint("Unique MCQ Subjects: $uniqueSubjects");
      } else {
        throw Exception("Failed to load MCQ subjects");
      }
    } catch (e) {
      setState(() {
        isLoading = false;
      });
      debugPrint("Error fetching MCQ subjects: $e");
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: CustomLogoAppBar(),
      body: Column(
        children: [
          Topbar(firstText: "MCQs", secondText: "Subjects"),
          Expanded(
            child: isLoading
                ? const Center(child: CircularProgressIndicator())
                : ListView.builder(
                    itemCount: mcqSubjects.length,
                    itemBuilder: (context, index) {
                      final subject = mcqSubjects[index];

                      return InkWell(
                        onTap: () {
                          Navigator.push(
                            context,
                            MaterialPageRoute(
                              builder: (context) => McqModulesScreen(
                                subjectName: subject.subjectName,
                              ),
                            ),
                          );
                        },
                        borderRadius: BorderRadius.circular(10),
                        child: Container(
                          margin: const EdgeInsets.symmetric(
                            horizontal: 16,
                            vertical: 8,
                          ),
                          decoration: BoxDecoration(
                            color: Colors.white,
                            borderRadius: BorderRadius.circular(10),
                            boxShadow: [
                              BoxShadow(
                                color: Colors.grey.withOpacity(0.2),
                                spreadRadius: 1,
                                blurRadius: 5,
                                offset: const Offset(0, 2),
                              ),
                            ],
                          ),
                          child: Column(
                            children: [
                              Padding(
                                padding: const EdgeInsets.all(16.0),
                                child: Row(
                                  mainAxisAlignment:
                                      MainAxisAlignment.spaceBetween,
                                  children: [
                                    Text(
                                      subject.subjectName,
                                      style: const TextStyle(
                                        fontWeight: FontWeight.bold,
                                        fontSize: 20,
                                        color: Colors.black54,
                                      ),
                                    ),
                                    Text(
                                      "${subject.moduleCount} MCQs",
                                      style: const TextStyle(
                                        color: Colors.grey,
                                      ),
                                    ),
                                  ],
                                ),
                              ),
                              // Bottom colored bar
                              Container(
                                height: 6,
                                decoration: BoxDecoration(
                                  color: Colors.teal.shade700,
                                  borderRadius: const BorderRadius.only(
                                    bottomLeft: Radius.circular(10),
                                    bottomRight: Radius.circular(10),
                                  ),
                                ),
                              ),
                            ],
                          ),
                        ),
                      );
                    },
                  ),
          ),
        ],
      ),
    );
  }
}
