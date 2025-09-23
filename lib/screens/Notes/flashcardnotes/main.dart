import 'package:flutter/material.dart';
import 'dart:convert';
import 'package:http/http.dart' as http;
import 'package:frontend/screens/notes/constants.dart';
import 'package:frontend/screens/notes/flashcardnotes/sub.dart'; // This should contain FlashcardDetailScreen
import 'package:frontend/screens/notes/logo.dart';
import 'package:frontend/screens/notes/topbar.dart';

// 1. DATA MODELS
class FlashcardImage {
  final int id;
  final String imageUrl;
  final String caption;

  FlashcardImage({
    required this.id,
    required this.imageUrl,
    required this.caption,
  });

  factory FlashcardImage.fromJson(Map<String, dynamic> json) {
    return FlashcardImage(
      id: json['id'] ?? 0,
      imageUrl: json['image'] ?? '',
      caption: json['caption'] ?? '',
    );
  }
}

class FlashcardSet {
  final int id;
  final String subjectName;
  final String description;
  final List<FlashcardImage> images;

  FlashcardSet({
    required this.id,
    required this.subjectName,
    required this.description,
    required this.images,
  });

  factory FlashcardSet.fromJson(Map<String, dynamic> json) {
    var imagesFromJson = json['images'] as List? ?? [];
    List<FlashcardImage> imageList =
        imagesFromJson.map((img) => FlashcardImage.fromJson(img)).toList();

    return FlashcardSet(
      id: json['id'] ?? 0,
      subjectName: json['subject_name'] ?? 'No Subject',
      description: json['description'] ?? '',
      images: imageList,
    );
  }
}

// 2. MAIN WIDGET: Shows all subjects
class FlashcardsScreen extends StatefulWidget {
  const FlashcardsScreen({super.key});

  @override
  State<FlashcardsScreen> createState() => _FlashcardsScreenState();
}

class _FlashcardsScreenState extends State<FlashcardsScreen> {
  bool _isLoading = true;
  String _errorMessage = '';
  Map<String, int> _subjectCounts = {}; // subject -> number of cards

  @override
  void initState() {
    super.initState();
    _fetchAndProcessFlashcards();
  }

  Future<void> _fetchAndProcessFlashcards() async {
    try {
      final url = Uri.parse("${API}flashcards/");
      final response = await http.get(url).timeout(const Duration(seconds: 15));

      if (!mounted) return;

      if (response.statusCode == 200) {
        final Map<String, dynamic> decoded = jsonDecode(response.body);

        // Access the list inside "results"
        final List<dynamic> allFlashcardSets = decoded['results'] ?? [];

        // Count cards per subject
        final Map<String, int> counts = {};
        for (var set in allFlashcardSets) {
          final subject = set['subject_name'] ?? 'Unknown';
          final List images = set['images'] ?? [];
          counts[subject] = (counts[subject] ?? 0) + images.length;
        }

        setState(() {
          _subjectCounts = counts;
          _isLoading = false;
        });
      } else {
        setState(() {
          _errorMessage = "Failed to load data (Code: ${response.statusCode})";
          _isLoading = false;
        });
      }
    } catch (e) {
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
      backgroundColor: const Color(0xFFF5F5F5),
      body: _buildBody(),
    );
  }

  Widget _buildBody() {
    if (_isLoading) {
      return const Center(child: CircularProgressIndicator());
    }
    if (_errorMessage.isNotEmpty) {
      return Center(
        child: Text(
          _errorMessage,
          style: const TextStyle(color: Colors.red, fontSize: 16),
        ),
      );
    }

    final subjectEntries = _subjectCounts.entries.toList();

    return Column(
      children: [
        Topbar(firstText: "Flash Card", secondText: "Subjects"),
        Expanded(
          child: ListView.builder(
            padding: const EdgeInsets.all(12.0),
            itemCount: subjectEntries.length,
            itemBuilder: (context, index) {
              final entry = subjectEntries[index];
              final subjectName = entry.key;
              final count = entry.value;

              return Padding(
                padding: const EdgeInsets.only(bottom: 12.0),
                child: InkWell(
                  onTap: () {
                    Navigator.push(
                      context,
                      MaterialPageRoute<void>(
                        builder: (context) =>
                            FlashcardDetailScreen(subjectName: subjectName),
                      ),
                    );
                  },
                  child: Card(
                    elevation: 1,
                    color: Colors.white,
                    shape: RoundedRectangleBorder(
                      borderRadius: BorderRadius.circular(8),
                    ),
                    margin: EdgeInsets.zero,
                    child: Column(
                      crossAxisAlignment: CrossAxisAlignment.start,
                      children: [
                        Padding(
                          padding: const EdgeInsets.fromLTRB(16, 16, 16, 20),
                          child: Row(
                            mainAxisAlignment: MainAxisAlignment.spaceBetween,
                            children: [
                              Text(
                                subjectName,
                                style: const TextStyle(
                                  fontWeight: FontWeight.w600,
                                  fontSize: 20,
                                  color: Colors.black87,
                                ),
                              ),
                              Text(
                                '$count ${count == 1 ? "Card" : "Cards"}',
                                style: const TextStyle(
                                  fontWeight: FontWeight.w400,
                                  fontSize: 20,
                                  color: Colors.black,
                                ),
                              ),
                            ],
                          ),
                        ),
                        Container(
                          height: 15,
                          decoration: const BoxDecoration(
                            color: Color(0xFF00897B),
                            borderRadius: BorderRadius.only(
                              bottomLeft: Radius.circular(8),
                              bottomRight: Radius.circular(8),
                            ),
                          ),
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
