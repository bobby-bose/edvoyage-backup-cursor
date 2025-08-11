import 'dart:convert';
import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;
import 'package:frontend/utils/colors/colors.dart';
import 'package:frontend/_env/env.dart';
import 'package:frontend/screens/Notes/mcqnotes/sub/main.dart';
import 'package:frontend/widgets/botttom_nav.dart';

class MCQNotesScreen extends StatefulWidget {
  const MCQNotesScreen({super.key});

  @override
  _MCQNotesScreenState createState() => _MCQNotesScreenState();
}

class _MCQNotesScreenState extends State<MCQNotesScreen> {
  late Future<List<Map<String, dynamic>>> mcqTopicsFuture;
  int _selectedIndex = 3; // Notes tab is active

  @override
  void initState() {
    super.initState();
    mcqTopicsFuture = fetchMCQTopics();
  }

  /// Fetches MCQ topics data from the API
  /// API Endpoint: GET /api/v1/notes/categories/mcq/topics/
  Future<List<Map<String, dynamic>>> fetchMCQTopics() async {
    try {
      final response = await http.get(
        Uri.parse('${BaseUrl.baseUrl}/notes/mcq/categories/'),
        headers: {
          'Content-Type': 'application/json',
          'Accept': 'application/json',
        },
      );

      print('MCQ Categories API Response Status: ${response.statusCode}');
      print('MCQ Categories API Response Body: ${response.body}');

      if (response.statusCode == 200) {
        final List<dynamic> data = json.decode(response.body);

        return data.map<Map<String, dynamic>>((item) {
          return {
            'id': item['id'],
            'title': item['name'],
            'description': '${item['question_count']} Questions',
            'modules_count': item['question_count'],
            'is_featured': false,
            'order': item['id'],
          };
        }).toList();
      } else {
        print('❌ API Error: ${response.statusCode}');
        return [];
      }
    } catch (e) {
      print('❌ Error fetching MCQ topics: $e');
      return [];
    }
  }

  /// Navigate to MCQ sub screen
  void _navigateToMCQSubScreen(Map<String, dynamic> topic) {
    Navigator.push(
      context,
      MaterialPageRoute(
        builder: (context) => MCQNotesSubScreen(
          categoryTitle: topic['title'] ?? 'Unknown Topic',
          categoryId: topic['id'] ?? 1,
        ),
      ),
    );
  }

  /// Builds individual MCQ topic cards
  Widget _buildMCQTopicCard(Map<String, dynamic> topic) {
    return GestureDetector(
      onTap: () => _navigateToMCQSubScreen(topic),
      child: Container(
        margin: EdgeInsets.symmetric(horizontal: 20, vertical: 4),
        decoration: BoxDecoration(
          color: whiteColor,
          borderRadius: BorderRadius.circular(8),
          border: Border(
            bottom: BorderSide(
              color: grey1,
              width: 1,
            ),
          ),
        ),
        child: Padding(
          padding: EdgeInsets.symmetric(horizontal: 16, vertical: 12),
          child: Row(
            children: [
              Expanded(
                child: Text(
                  topic['title'] ?? 'Unknown Topic',
                  style: TextStyle(
                    fontFamily: 'Poppins',
                    fontSize: 16,
                    fontWeight: FontWeight.w500,
                    color: titlecolor,
                  ),
                ),
              ),
              Row(
                children: [
                  Text(
                    '${topic['modules_count'] ?? 0} Modules',
                    style: TextStyle(
                      fontFamily: 'Poppins',
                      fontSize: 14,
                      color: grey3,
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
          _buildNavItem(0, 'assets/frame.png', 'Profile'),
          _buildNavItem(1, 'assets/diamonds.png', 'Diamond'),
          _buildNavItem(2, 'assets/Group 98.png', 'Y'),
          _buildNavItem(3, 'assets/book.png', 'Notes', isActive: true),
          _buildNavItem(4, 'assets/airplane.png', 'Travel'),
        ],
      ),
    );
  }

  /// Builds individual navigation items
  Widget _buildNavItem(int index, String iconPath, String label,
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
          ImageIcon(
            AssetImage(iconPath),
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
        backgroundColor: primaryColor,
        title: Text(
          'MCQ Notes',
          style: TextStyle(
            fontFamily: 'Poppins',
            fontSize: 20,
            fontWeight: FontWeight.bold,
            color: whiteColor,
          ),
        ),
        centerTitle: true,
        elevation: 0,
      ),
      body: SafeArea(
        child: Column(
          children: [
            Expanded(
              child: FutureBuilder<List<Map<String, dynamic>>>(
                future: mcqTopicsFuture,
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
                            'Loading MCQs...',
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
                    print('❌ Snapshot Error: ${snapshot.error}');
                    return Center(
                      child: Text(
                        'Failed to load MCQs',
                        style: TextStyle(
                          fontFamily: 'Poppins',
                          fontSize: 16,
                          color: grey3,
                        ),
                      ),
                    );
                  }

                  final topics = snapshot.data ?? [];
                  if (topics.isEmpty) {
                    print('⚠️ No MCQ data received from API');
                    return Center(
                      child: Text(
                        'NoDataReceived', // Your desired placeholder
                        style: TextStyle(
                          fontFamily: 'Poppins',
                          fontSize: 16,
                          color: grey3,
                        ),
                      ),
                    );
                  }
                  return ListView.builder(
                    padding: EdgeInsets.symmetric(vertical: 8),
                    itemCount: topics.length,
                    itemBuilder: (context, index) {
                      return _buildMCQTopicCard(topics[index]);
                    },
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
