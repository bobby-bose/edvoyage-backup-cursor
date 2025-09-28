import 'package:flutter/material.dart';
import 'dart:convert';
import 'package:http/http.dart' as http;
import 'package:frontend/screens/notes/constants.dart';
import 'package:frontend/screens/notes/logo.dart';
import 'package:frontend/screens/notes/topbar.dart';

// DATA MODEL
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

// MAIN WIDGET for the detail screen
class FlashcardDetailScreen extends StatefulWidget {
  final String subjectName;
  final String className;
  const FlashcardDetailScreen(
      {super.key, required this.subjectName, required this.className});

  @override
  State<FlashcardDetailScreen> createState() => _FlashcardDetailScreenState();
}

class _FlashcardDetailScreenState extends State<FlashcardDetailScreen> {
  bool _isLoading = true;
  String _errorMessage = '';
  List<FlashcardImage> _images = [];
  final PageController _pageController = PageController();
  int _currentIndex = 0;

  @override
  void initState() {
    super.initState();
    _fetchAndFilterImages();
  }

  @override
  void dispose() {
    _pageController.dispose();
    super.dispose();
  }

  Future<void> _fetchAndFilterImages() async {
    try {
      final url = Uri.parse("${API}flashcards/");
      final response = await http.get(url).timeout(const Duration(seconds: 15));

      if (!mounted) return;

      if (response.statusCode == 200) {
        final decoded = jsonDecode(response.body) as Map<String, dynamic>;

        // ✅ Extract list from "results"
        final List<dynamic> allFlashcardSets = decoded['results'] ?? [];

        // ✅ Find the specific flashcard set
        final flashcardSetData = allFlashcardSets.firstWhere(
          (set) =>
              set['subject_name'] == widget.subjectName &&
              set['category']?['name'] == widget.className,
          orElse: () => null,
        );

        if (flashcardSetData != null) {
          final List<dynamic> imagesJson = flashcardSetData['images'] ?? [];
          setState(() {
            _images =
                imagesJson.map((img) => FlashcardImage.fromJson(img)).toList();
            _isLoading = false;
          });
        } else {
          setState(() {
            _errorMessage = "No flashcards found for '${widget.subjectName}'.";
            _isLoading = false;
          });
        }
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
      backgroundColor: Colors.white,
      appBar: CustomLogoAppBar(),
      body: _buildBody(),
    );
  }

  Widget _buildBody() {
    if (_isLoading) {
      return const Center(child: CircularProgressIndicator());
    }
    if (_errorMessage.isNotEmpty) {
      return Center(
        child: Text(_errorMessage, style: const TextStyle(color: Colors.red)),
      );
    }
    if (_images.isEmpty) {
      return const Center(child: Text("No images found for this subject."));
    }

    return Column(
      children: [
        Topbar(firstText: "Flash Card", secondText: widget.subjectName),
        Expanded(
          child: PageView.builder(
            controller: _pageController,
            itemCount: _images.length,
            onPageChanged: (index) {
              setState(() {
                _currentIndex = index;
              });
            },
            itemBuilder: (context, index) {
              final image = _images[index];
              return _buildFlashcard(image);
            },
          ),
        ),
        _buildFooter(),
      ],
    );
  }

  Widget _buildFlashcard(FlashcardImage image) {
    debugPrint("Image URL: ${image.imageUrl}");

    return Padding(
      padding: const EdgeInsets.all(16.0),
      child: Card(
        elevation: 0,
        shape: RoundedRectangleBorder(
          borderRadius: BorderRadius.circular(16),
          side: BorderSide(color: Colors.grey.shade300),
        ),
        child: SingleChildScrollView(
          padding: const EdgeInsets.all(20.0),
          child: Column(
            children: [
              const SizedBox(height: 20),
              ClipRRect(
                borderRadius: BorderRadius.circular(12),
                child: Image.network(
                  image.imageUrl,
                  fit: BoxFit.contain,
                  errorBuilder: (context, error, stackTrace) => const Center(
                    child:
                        Icon(Icons.broken_image, size: 50, color: Colors.grey),
                  ),
                ),
              ),
            ],
          ),
        ),
      ),
    );
  }

  Widget _buildFooter() {
    bool isLastImage = _currentIndex == _images.length - 1;

    return Container(
      padding: const EdgeInsets.symmetric(horizontal: 24.0, vertical: 20.0),
      decoration: BoxDecoration(
        color: Colors.white,
        border: Border(top: BorderSide(color: Colors.grey.shade300)),
      ),
      child: Row(
        mainAxisAlignment: MainAxisAlignment.spaceBetween,
        children: [
          ElevatedButton(
            onPressed: _currentIndex > 0
                ? () {
                    _pageController.previousPage(
                      duration: const Duration(milliseconds: 300),
                      curve: Curves.easeIn,
                    );
                  }
                : null,
            style: ElevatedButton.styleFrom(
              backgroundColor: const Color(0xFF008080),
              padding: const EdgeInsets.symmetric(horizontal: 30, vertical: 12),
            ),
            child: const Text('PREV',
                style: TextStyle(
                    fontWeight: FontWeight.bold, color: Colors.white)),
          ),
          Text(
            '${_currentIndex + 1} / ${_images.length}',
            style: const TextStyle(fontWeight: FontWeight.bold, fontSize: 25),
          ),
          ElevatedButton(
            onPressed: () {
              if (isLastImage) {
                Navigator.of(context).pop();
              } else {
                _pageController.nextPage(
                  duration: const Duration(milliseconds: 300),
                  curve: Curves.easeIn,
                );
              }
            },
            style: ElevatedButton.styleFrom(
              backgroundColor: const Color(0xFF008080),
              padding: const EdgeInsets.symmetric(horizontal: 30, vertical: 12),
            ),
            child: Text(
              isLastImage ? 'FINISH' : 'NEXT',
              style: const TextStyle(
                  fontWeight: FontWeight.bold, color: Colors.white),
            ),
          ),
        ],
      ),
    );
  }
}
