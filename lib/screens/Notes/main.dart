import 'dart:convert';
import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;
import 'package:frontend/utils/colors/colors.dart';
import 'package:frontend/_env/env.dart';
import 'package:frontend/screens/Notes/videonotes/main.dart';
import 'package:frontend/screens/Notes/mcqnotes/main.dart';
import 'package:frontend/screens/Notes/clinicalnotes/main.dart';
import 'package:frontend/screens/Notes/questionbanknotes/main.dart';
import 'package:frontend/screens/Notes/flashcardnotes/main.dart';
import 'package:frontend/widgets/botttom_nav.dart';

class NotesSection extends StatefulWidget {
  const NotesSection({super.key});

  @override
  _NotesSectionState createState() => _NotesSectionState();
}

class _NotesSectionState extends State<NotesSection> {
  late Future<Map<String, dynamic>> notesDataFuture;
  int _selectedIndex = 3; // Notes tab is active

  @override
  void initState() {
    super.initState();
    notesDataFuture = fetchNotesData();
  }

  /// Fetches notes categories data from the API
  /// API Endpoint: GET /api/v1/notes/categories/
  Future<Map<String, dynamic>> fetchNotesData() async {
    try {
      final response = await http.get(
        Uri.parse('${BaseUrl.baseUrl}/notes/categories/'),
        headers: {
          'Content-Type': 'application/json',
          'Accept': 'application/json',
        },
      );

      print('Notes API Response Status: ${response.statusCode}');
      print('Notes API Response Body: ${response.body}');

      if (response.statusCode == 200) {
        final data = json.decode(response.body);

        // Check if the response has the expected structure
        if (data['status'] == 'success' && data['data'] != null) {
          print('Successfully fetched notes data from API');
          return data['data'];
        } else {
          print('API Response structure unexpected: $data');
          throw Exception('Invalid API response structure');
        }
      } else {
        print('API Error: ${response.statusCode} - ${response.body}');
        throw Exception('Failed to load notes data: ${response.statusCode}');
      }
    } catch (e) {
      print('Error fetching notes data: $e');
      // Return default data structure if API fails
      return {
        'video': {'topics': 0, 'videos': 0},
        'mcq': {'topics': 0, 'modules': 0},
        'clinical_case': {'topics': 0, 'modules': 0},
        'q_bank': {'topics': 0, 'modules': 0},
        'flash_card': {'topics': 0, 'modules': 0},
      };
    }
  }

  /// Formats count values for display
  /// Returns '-' for null/empty, '0' for zero, or the actual count
  String _formatCount(dynamic count) {
    if (count == null || count == '') return '-';
    if (count == 0) return '0';
    return count.toString();
  }

  /// Navigate to Video Notes screen
  void _navigateToVideoNotes() {
    Navigator.push(
      context,
      MaterialPageRoute(
        builder: (context) => VideoNotesScreen(),
      ),
    );
  }

  /// Navigate to MCQ Notes screen
  void _navigateToMCQNotes() {
    Navigator.push(
      context,
      MaterialPageRoute(
        builder: (context) => MCQNotesScreen(),
      ),
    );
  }

  /// Navigate to Clinical Notes screen
  void _navigateToClinicalNotes() {
    Navigator.push(
      context,
      MaterialPageRoute(
        builder: (context) => ClinicalNotesScreen(),
      ),
    );
  }

  /// Navigate to Q-Bank Notes screen
  void _navigateToQBankNotes() {
    Navigator.push(
      context,
      MaterialPageRoute(
        builder: (context) => QuestionBankNotesScreen(),
      ),
    );
  }

  /// Navigate to Flash Card Notes screen
  void _navigateToFlashCardNotes() {
    Navigator.push(
      context,
      MaterialPageRoute(
        builder: (context) => FlashCardNotesScreen(),
      ),
    );
  }

  /// Builds individual content cards for each category
  Widget _buildContentCard({
    required String title,
    required String topicsCount,
    required String modulesCount,
    required String modulesLabel,
    required VoidCallback onTap,
  }) {
    return GestureDetector(
      onTap: onTap,
      child: Container(
        margin: EdgeInsets.symmetric(horizontal: 20, vertical: 8),
        decoration: BoxDecoration(
          color: whiteColor,
          borderRadius: BorderRadius.circular(12),
          boxShadow: [
            BoxShadow(
              color: Colors.black.withOpacity(0.05),
              blurRadius: 10,
              offset: Offset(0, 2),
            ),
          ],
        ),
        child: Padding(
          padding: EdgeInsets.all(20),
          child: Row(
            children: [
              Expanded(
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    Text(
                      title,
                      style: TextStyle(
                        fontFamily: 'Poppins',
                        fontSize: 18,
                        fontWeight: FontWeight.w600,
                        color: titlecolor,
                      ),
                    ),
                    SizedBox(height: 4),
                    Text(
                      '$topicsCount Topics',
                      style: TextStyle(
                        fontFamily: 'Poppins',
                        fontSize: 14,
                        color: grey3,
                      ),
                    ),
                  ],
                ),
              ),
              Row(
                children: [
                  Text(
                    '$modulesCount $modulesLabel',
                    style: TextStyle(
                      fontFamily: 'Poppins',
                      fontSize: 12,
                      color: primaryColor,
                      fontWeight: FontWeight.w500,
                    ),
                  ),
                  SizedBox(width: 8),
                  Icon(
                    Icons.arrow_forward_ios,
                    color: grey3,
                    size: 16,
                  ),
                ],
              ),
            ],
          ),
        ),
      ),
    );
  }

  /// Builds bottom navigation bar
  Widget _buildBottomNavigation() {
    return Container(
      height: 250,
      decoration: BoxDecoration(
        color: primaryColor,
        borderRadius: BorderRadius.only(
          topLeft: Radius.circular(20),
          topRight: Radius.circular(20),
        ),
      ),
      child: Row(
        mainAxisAlignment: MainAxisAlignment.spaceEvenly,
        children: [
          _buildNavItem(0, Icons.person_outline, 'Profile'),
          _buildNavItem(1, Icons.diamond_outlined, 'Diamond'),
          _buildNavItem(2, Icons.text_fields, 'Y'),
          _buildNavItem(3, Icons.book, 'Notes', isActive: true),
          _buildNavItem(4, Icons.flight, 'Travel'),
        ],
      ),
    );
  }

  /// Builds individual navigation items
  Widget _buildNavItem(int index, IconData icon, String label,
      {bool isActive = false}) {
    return GestureDetector(
      onTap: () {
        setState(() {
          _selectedIndex = index;
        });
      },
      child: Column(
        mainAxisAlignment: MainAxisAlignment.center,
        children: [
          Icon(
            icon,
            color: isActive ? secondaryColor : whiteColor,
            size: 24,
          ),
          if (isActive)
            Container(
              margin: EdgeInsets.only(top: 4),
              height: 2,
              width: 20,
              decoration: BoxDecoration(
                color: secondaryColor,
                borderRadius: BorderRadius.circular(1),
              ),
            ),
        ],
      ),
    );
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: color3,
      appBar: AppBar(
        backgroundColor: Colors.white,
        elevation: 0,
        leading: IconButton(
          icon: Icon(Icons.arrow_back, color: Colors.blue),
          onPressed: () => Navigator.pop(context),
        ),
        title: Image.asset(
          'assets/logo.png',
          height: 250,
          width: 250,
          fit: BoxFit.contain,
          errorBuilder: (context, error, stackTrace) {
            return Icon(
              Icons.book,
              color: Colors.blue,
              size: 24,
            );
          },
        ),
        centerTitle: true,
      ),
      body: SafeArea(
        child: Column(
          children: [
            Expanded(
              child: FutureBuilder<Map<String, dynamic>>(
                future: notesDataFuture,
                builder: (context, snapshot) {
                  if (snapshot.connectionState == ConnectionState.waiting) {
                    return Center(
                      child: Column(
                        mainAxisAlignment: MainAxisAlignment.center,
                        children: [
                          CircularProgressIndicator(
                            color: primaryColor,
                            strokeWidth: 2,
                          ),
                          SizedBox(height: 16),
                          Text(
                            'Loading Notes...',
                            style: TextStyle(
                              fontFamily: 'Poppins',
                              fontSize: 16,
                              color: grey3,
                            ),
                          ),
                        ],
                      ),
                    );
                  }

                  if (snapshot.hasError) {
                    return Center(
                      child: Column(
                        mainAxisAlignment: MainAxisAlignment.center,
                        children: [
                          Icon(
                            Icons.error_outline,
                            size: 48,
                            color: grey3,
                          ),
                          SizedBox(height: 16),
                          Text(
                            'Failed to load content',
                            style: TextStyle(
                              fontFamily: 'Poppins',
                              fontSize: 16,
                              color: grey3,
                            ),
                          ),
                          SizedBox(height: 8),
                          Text(
                            'Please check your connection',
                            style: TextStyle(
                              fontFamily: 'Poppins',
                              fontSize: 14,
                              color: grey3,
                            ),
                          ),
                          SizedBox(height: 16),
                          ElevatedButton(
                            onPressed: () {
                              setState(() {
                                notesDataFuture = fetchNotesData();
                              });
                            },
                            style: ElevatedButton.styleFrom(
                              backgroundColor: primaryColor,
                              shape: RoundedRectangleBorder(
                                borderRadius: BorderRadius.circular(8),
                              ),
                            ),
                            child: Text(
                              'Retry',
                              style: TextStyle(
                                fontFamily: 'Poppins',
                                color: whiteColor,
                                fontSize: 14,
                              ),
                            ),
                          ),
                        ],
                      ),
                    );
                  }

                  final data = snapshot.data ?? {};

                  return ListView(
                    padding: EdgeInsets.symmetric(vertical: 10),
                    children: [
                      _buildContentCard(
                        title: 'Video',
                        topicsCount: _formatCount(data['video']?['topics']),
                        modulesCount: _formatCount(data['video']?['videos']),
                        modulesLabel: 'Videos',
                        onTap: _navigateToVideoNotes,
                      ),
                      _buildContentCard(
                        title: 'MCQ',
                        topicsCount: _formatCount(data['mcq']?['topics']),
                        modulesCount: _formatCount(data['mcq']?['modules']),
                        modulesLabel: 'Modules',
                        onTap: _navigateToMCQNotes,
                      ),
                      _buildContentCard(
                        title: 'Clinical Case',
                        topicsCount:
                            _formatCount(data['clinical_case']?['topics']),
                        modulesCount:
                            _formatCount(data['clinical_case']?['modules']),
                        modulesLabel: 'Modules',
                        onTap: _navigateToClinicalNotes,
                      ),
                      _buildContentCard(
                        title: 'Q-Bank',
                        topicsCount: _formatCount(data['q_bank']?['topics']),
                        modulesCount: _formatCount(data['q_bank']?['modules']),
                        modulesLabel: 'Modules',
                        onTap: _navigateToQBankNotes,
                      ),
                      _buildContentCard(
                        title: 'Flash Card',
                        topicsCount:
                            _formatCount(data['flash_card']?['topics']),
                        modulesCount:
                            _formatCount(data['flash_card']?['modules']),
                        modulesLabel: 'Modules',
                        onTap: _navigateToFlashCardNotes,
                      ),
                    ],
                  );
                },
              ),
            ),
            BottomButton(onTap: () {}, selectedIndex: 3),
          ],
        ),
      ),
    );
  }
}
