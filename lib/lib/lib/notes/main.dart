import 'dart:convert';
import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;
import 'package:notes/screens/clinicalnotes/main.dart';
import 'package:notes/screens/constants.dart';
import 'package:notes/screens/flashcardnotes/main.dart';
import 'package:notes/screens/logo.dart';
import 'package:notes/screens/mcqnotes/main.dart';
import 'package:notes/screens/videonotes/main.dart';
import 'package:notes/widgets/explore_courses/app_bar.dart';

class NotesScreen extends StatefulWidget {
  final String className;
  const NotesScreen({super.key, required this.className});

  @override
  State<NotesScreen> createState() => _NotesScreenState();
}

class _NotesScreenState extends State<NotesScreen> {
  final bool _isLoading = false;
  int _VideoTotalCount = 0;
  int _VideoUniqueCount = 0;
  int _mcqCount = 0;
  int _mcqSubjectCount = 0;
  final int _clinicalCaseCount = 0;
  final int _flashcardTotalCount = 0;
  final int _flashcardUniqueCount = 0;
  int _subjectNamesCount = 0;
  int _clinicalTotalCount = 0;
  int _flashCardUniqueCount = 0;
  int _flashCardTotalCount = 0;

  @override
  void initState() {
    super.initState();
    _fetchVideoStats();
    _fetchMcqStats();
    _fetchClinicalCases();
    _fetchFlashCards();
  }

  Future<void> _fetchVideoStats() async {
    try {
      final response = await http.get(Uri.parse("${API}videos/"));

      if (response.statusCode == 200) {
        final List<dynamic> data = jsonDecode(response.body);

        int titleCount = data.length;

        int count = 0;

        var SubjectNames = data
            .where((video) => video['category']["name"] == widget.className)
            .map((video) => video['subject_name'])
            .toList()
            .toSet();

        var VideoUrls = data
            .where((video) => video['category']["name"] == widget.className)
            .map((video) => video['video_url'])
            .toList();

        print("The Video Urls are $VideoUrls");
        print("The Subject Names are $SubjectNames");
        int VideoUrlsCount = VideoUrls.length;
        int SubjectNamesCount = SubjectNames.length;
        print("The Video Urls Count is $VideoUrlsCount");
        print("The Subject Names Count is $SubjectNamesCount");

        setState(() {
          _VideoUniqueCount = SubjectNamesCount;
          _VideoTotalCount = VideoUrlsCount;
        });
      } else {
        print("Failed to load data. Status: ${response.statusCode}");
      }
    } catch (e) {
      print("Error fetching MCQ stats: $e");
    }
  }

  Future<void> _fetchMcqStats() async {
    try {
      final response = await http.get(Uri.parse("${API}mcqs/"));

      if (response.statusCode == 200) {
        final List<dynamic> data = jsonDecode(response.body);

        int titleCount = data.length;

        int count = 0;

        var SubjectNames = data
            .where((video) => video['category']["name"] == widget.className)
            .map((video) => video['subject']['name'])
            .toList()
            .toSet();

        var McqQuestions = data
            .where(
              (video) =>
                  video['category']["name"] == widget.className &&
                  video['questions'] != null &&
                  (video['questions'] as List).isNotEmpty,
            )
            .map((video) => video['questions'])
            .toList();

        print("The MCQ Questions are $McqQuestions");
        print("The Subject Names are $SubjectNames");
        int McqQuestionsCount = McqQuestions.length;
        int SubjectNamesCount = SubjectNames.length;
        print("The McQ Count is $McqQuestionsCount");
        print("The Subject Names Count is $SubjectNamesCount");

        setState(() {
          _mcqCount = McqQuestionsCount;
          _mcqSubjectCount = SubjectNamesCount;
        });
      } else {
        print("Failed to load data. Status: ${response.statusCode}");
      }
    } catch (e) {
      print("Error fetching MCQ stats: $e");
    }
  }

  Future<void> _fetchClinicalCases() async {
    try {
      final response = await http.get(Uri.parse("${API}clinical-cases/"));
      if (response.statusCode == 200) {
        final List<dynamic> data = jsonDecode(response.body);

        int titleCount = data.length;

        int count = 0;

        var SubjectNames = data
            .where((video) => video['category']["name"] == widget.className)
            .map((video) => video['subject_name'])
            .toList()
            .toSet();

        var clinicalCases = data
            .where((video) => video['category']["name"] == widget.className)
            .toList();

        print("The Clinical Cases  are $clinicalCases");
        print("The Subject Names are $SubjectNames");
        int clinicalCasesCount = clinicalCases.length;
        int SubjectNamesCount = SubjectNames.length;
        print("The clinicalCasesCount Count is $clinicalCasesCount");
        print("The Subject Names Count is $SubjectNamesCount");
        setState(() {
          _subjectNamesCount = SubjectNamesCount;
          _clinicalTotalCount = clinicalCasesCount;
        });
      }
    } catch (e) {
      print("Error fetching Clinical Cases: $e");
    }
  }

  Future<void> _fetchFlashCards() async {
    try {
      final response = await http.get(Uri.parse("${API}flashcards/"));
      if (response.statusCode == 200) {
        final List<dynamic> data = jsonDecode(response.body);
        int titleCount = data.length;

        int count = 0;

        var SubjectNames = data
            .where((video) => video['category']["name"] == widget.className)
            .map((video) => video['subject_name'])
            .toList()
            .toSet();

        var flashCards = data
            .where((video) => video['category']["name"] == widget.className)
            .toList();

        print("The Flash Cards are $flashCards");
        print("The Subject Names are $SubjectNames");
        int flashCardsCount = flashCards.length;
        int SubjectNamesCount = SubjectNames.length;
        print("The FlashcardCount Count is $flashCardsCount");
        print("The Subject Names Count is $SubjectNamesCount");

        setState(() {
          _flashCardUniqueCount = SubjectNamesCount;
          _flashCardTotalCount = flashCardsCount;
        });
      }
    } catch (e) {
      print("Error fetching Flashcards: $e");
    }
  }

  @override
  Widget build(BuildContext context) {
    const Color primaryColor = Color(0xFF008080);

    return Theme(
      data: Theme.of(context).copyWith(
        textTheme: Theme.of(context).textTheme.apply(
          fontFamily: "YourCustomFont", // add your font here
        ),
      ),
      child: Scaffold(
        backgroundColor: Colors.grey[100],
        appBar: CustomLogoAppBar(),
        body: SingleChildScrollView(
          child: Padding(
            padding: const EdgeInsets.all(16.0),
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                const SizedBox(height: 16),

                // Video Card
                NoteCard(
                  title: 'Video',
                  leftSubtitle: _isLoading
                      ? 'Loading...'
                      : '$_VideoUniqueCount Subjects',
                  rightSubtitle: _isLoading ? '' : '$_VideoTotalCount Videos',
                  navigateTo: const VideoSubjectScreen(),
                ),

                // MCQ Card
                NoteCard(
                  title: 'MCQs',
                  leftSubtitle: _isLoading
                      ? 'Loading...'
                      : '$_mcqSubjectCount Topics',
                  rightSubtitle: _isLoading ? '' : '$_mcqCount MCQs',
                  navigateTo: const McqSubjectsScreen(),
                ),

                // Clinical Case Card
                NoteCard(
                  title: 'Clinical Case',
                  leftSubtitle: _isLoading
                      ? 'Loading...'
                      : '$_subjectNamesCount Subjects',
                  rightSubtitle: _isLoading
                      ? ''
                      : '$_clinicalTotalCount Clinical Cases',
                  navigateTo: const ClinicalCasesScreen(),
                ),

                // Flash Card
                NoteCard(
                  title: 'Flash Card',
                  leftSubtitle: _isLoading
                      ? 'Loading...'
                      : '$_flashCardUniqueCount Subjects',
                  rightSubtitle: _isLoading
                      ? ''
                      : '$_flashCardTotalCount Flash Cards',
                  navigateTo: const FlashcardsScreen(),
                ),
              ],
            ),
          ),
        ),
      ),
    );
  }
}

class NoteCard extends StatelessWidget {
  final String title;
  final String leftSubtitle;
  final String rightSubtitle;
  final Widget navigateTo;

  const NoteCard({
    super.key,
    required this.title,
    required this.leftSubtitle,
    required this.rightSubtitle,
    required this.navigateTo,
  });

  @override
  Widget build(BuildContext context) {
    const Color primaryColor = Color(0xFF008080);

    return GestureDetector(
      onTap: () {
        Navigator.push(
          context,
          MaterialPageRoute(builder: (context) => navigateTo),
        );
      },
      child: Padding(
        padding: const EdgeInsets.symmetric(vertical: 8.0),
        child: Card(
          elevation: 2,
          clipBehavior: Clip.antiAlias,
          shape: RoundedRectangleBorder(
            borderRadius: BorderRadius.circular(16.0),
          ),
          child: SizedBox(
            height: 160,
            width: double.infinity,
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                ListTile(
                  title: Text(
                    title,
                    style: const TextStyle(
                      fontSize: 22,
                      fontWeight: FontWeight.bold,
                    ),
                  ),
                  trailing: const Icon(Icons.more_vert),
                ),
                const Spacer(),
                Padding(
                  padding: const EdgeInsets.symmetric(horizontal: 16.0),
                  child: Row(
                    mainAxisAlignment: MainAxisAlignment.spaceBetween,
                    children: [
                      Text(
                        leftSubtitle,
                        style: const TextStyle(
                          color: Colors.black54,
                          fontSize: 20,
                          fontWeight: FontWeight.w600,
                        ),
                      ),
                      Text(
                        rightSubtitle,
                        style: const TextStyle(
                          color: primaryColor,
                          fontWeight: FontWeight.w600,
                          fontSize: 20,
                        ),
                      ),
                    ],
                  ),
                ),
                const SizedBox(height: 12),
                Container(
                  height: 20,
                  width: double.infinity,
                  color: primaryColor,
                ),
              ],
            ),
          ),
        ),
      ),
    );
  }
}
