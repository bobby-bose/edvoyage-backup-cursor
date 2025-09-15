import 'dart:convert';
import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;
import 'package:notes/screens/constants.dart';
import 'package:notes/screens/logo.dart';
import 'package:notes/screens/mcqnotes/mcq.dart';
import 'package:notes/screens/topbar.dart';

// 1. Model Class for the MCQ Module (No changes needed here)
class McqModule {
  final int id;
  final String title;
  final String subjectName;
  final bool isFree;
  final String logoUrl;
  final int questionCount;

  McqModule({
    required this.id,
    required this.title,
    required this.subjectName,
    required this.isFree,
    required this.logoUrl,
    required this.questionCount,
  });

  factory McqModule.fromJson(Map<String, dynamic> json) {
    final questions = json['questions'] as List<dynamic>?;
    print("Module ${json['id']} has ${questions?.length ?? 0} questions");

    return McqModule(
      id: json['id'] ?? 0,
      title: json['title'] ?? 'No Title',
      subjectName: json['subject']?['name'] ?? 'Unknown Subject',
      isFree: json['is_free'] ?? false,
      logoUrl: json['logo'] ?? '',
      questionCount: questions?.length ?? 0, // ✅ counts properly
    );
  }
}

// 2. StatefulWidget for the Screen
class McqModulesScreen extends StatefulWidget {
  final String subjectName;

  const McqModulesScreen({super.key, required this.subjectName});

  @override
  State<McqModulesScreen> createState() => _McqModulesScreenState();
}

class _McqModulesScreenState extends State<McqModulesScreen> {
  bool _isLoading = true;
  List<McqModule> _filteredModules = [];
  String _errorMessage = ''; // Variable to hold error messages for the UI

  @override
  void initState() {
    super.initState();
    _fetchAndFilterModules();
  }

  // 3. Method to fetch and filter data
  Future<void> _fetchAndFilterModules() async {
    final url = Uri.parse("${API}mcqs/");

    try {
      final response = await http.get(url).timeout(const Duration(seconds: 10));

      // ✅ IMPROVEMENT: Check if the widget is still in the tree before calling setState
      if (!mounted) return;

      if (response.statusCode == 200) {
        final List<dynamic> data = jsonDecode(response.body);
        final List<McqModule> modules = data
            .map((json) => McqModule.fromJson(json))
            .where((module) => module.subjectName == widget.subjectName)
            .toList();

        setState(() {
          _filteredModules = modules;
          _isLoading = false;
        });
      } else {
        // Handle server errors more gracefully
        setState(() {
          _errorMessage = "Failed to load data (Code: ${response.statusCode})";
          _isLoading = false;
        });
      }
    } catch (e) {
      // Handle network or other errors more gracefully
      if (!mounted) return;
      setState(() {
        _errorMessage = "An error occurred: $e";
        _isLoading = false;
      });
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: CustomLogoAppBar(),
      // ✅ IMPROVEMENT: Better UI feedback for loading, empty, and error states
      body: _buildBody(),
    );
  }

  Widget _buildBody() {
    if (_isLoading) {
      return const Center(child: CircularProgressIndicator());
    }

    if (_errorMessage.isNotEmpty) {
      return Center(
        child: Padding(
          padding: const EdgeInsets.all(16.0),
          child: Text(
            _errorMessage,
            textAlign: TextAlign.center,
            style: const TextStyle(color: Colors.red, fontSize: 16),
          ),
        ),
      );
    }

    if (_filteredModules.isEmpty) {
      return const Center(
        child: Text(
          "No modules found for this subject.",
          style: TextStyle(fontSize: 16),
        ),
      );
    }

    // ✅ FIX: The itemBuilder is now correctly placed inside a ListView.builder widget.
    return Column(
      children: [
        Topbar(firstText: "MCQ", secondText: widget.subjectName),
        Expanded(
          child: ListView.builder(
            padding: const EdgeInsets.all(8.0),
            itemCount: _filteredModules.length,
            itemBuilder: (context, index) {
              final module = _filteredModules[index];
              return Card(
                elevation: 3,
                margin: const EdgeInsets.symmetric(
                  vertical: 8.0,
                  horizontal: 4.0,
                ),
                shape: RoundedRectangleBorder(
                  borderRadius: BorderRadius.circular(12),
                  side: BorderSide(color: Colors.grey.shade300, width: 1),
                ),
                clipBehavior: Clip
                    .antiAlias, // Ensures the InkWell ripple respects the border radius
                child: InkWell(
                  onTap: () {
                    // TODO: Navigate to the quiz screen for this module
                    // debugPrint("Tapped on module ID: ${module.id}");
                    // code to navigate to the flutetr widget adn pass a parameter
                    Navigator.push(
                      context,
                      MaterialPageRoute(
                        builder: (context) =>
                            QuizScreen(moduleTitle: module.title),
                      ),
                    );
                  },
                  child: Padding(
                    padding: const EdgeInsets.all(12.0),
                    child: Row(
                      children: [
                        // 1. Left Side: Image
                        ClipRRect(
                          borderRadius: BorderRadius.circular(8.0),
                          child: SizedBox(
                            width: 100,
                            height: 100,
                            child: Image.network(
                              module.logoUrl,
                              fit: BoxFit.cover,
                              // Placeholder while loading
                              loadingBuilder:
                                  (context, child, loadingProgress) {
                                    if (loadingProgress == null) return child;
                                    return const Center(
                                      child: CircularProgressIndicator(
                                        strokeWidth: 2.0,
                                      ),
                                    );
                                  },
                              // Placeholder for errors
                              errorBuilder: (context, error, stackTrace) {
                                return Container(
                                  color: Colors.grey.shade200,
                                  child: const Icon(
                                    Icons.school,
                                    color: Colors.grey,
                                  ),
                                );
                              },
                            ),
                          ),
                        ),
                        const SizedBox(width: 16),

                        // 2. Middle Section: Title and Subtitle
                        Expanded(
                          child: Column(
                            crossAxisAlignment: CrossAxisAlignment.start,
                            children: [
                              Text(
                                module.title,
                                style: const TextStyle(
                                  fontWeight: FontWeight.bold,
                                  fontSize: 25,
                                  color: Color(0xFF008080), // Teal color
                                ),
                              ),
                              const SizedBox(height: 8),
                              Row(
                                children: [
                                  Icon(
                                    Icons.timer_outlined,
                                    color: Colors.grey.shade600,
                                    size: 22,
                                  ),
                                  const SizedBox(width: 4),
                                  Text(
                                    "${module.questionCount} MCQ's",
                                    style: TextStyle(
                                      color: Colors.grey.shade700,
                                      fontSize: 22,
                                    ),
                                  ),
                                ],
                              ),
                            ],
                          ),
                        ),
                        const SizedBox(width: 8),

                        // 3. Right Side: Free/Locked Status
                        // 3. Right Side: Crown or Lock image from assets
                        Image.asset(
                          module.isFree
                              ? 'assets/crown.png'
                              : 'assets/lock.png',
                          width: 40,
                          height: 40,
                        ),
                      ],
                    ),
                  ),
                ),
              );
            },
          ),
        ),
      ],
    );
  }
}
