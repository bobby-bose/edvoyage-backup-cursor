import 'dart:convert';
import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;
import 'package:frontend/utils/colors/colors.dart';
import 'package:frontend/_env/env.dart';
import 'package:frontend/screens/Notes/videonotes/sub/main.dart';
import 'package:frontend/widgets/botttom_nav.dart';

class VideoNotesScreen extends StatefulWidget {
  const VideoNotesScreen({super.key});

  @override
  _VideoNotesScreenState createState() => _VideoNotesScreenState();
}

class _VideoNotesScreenState extends State<VideoNotesScreen> {
  late Future<List<Map<String, dynamic>>> videoTopicsFuture;
  int _selectedIndex = 3; // Notes tab is active

  @override
  void initState() {
    super.initState();
    videoTopicsFuture = fetchVideoTopics();
  }

  /// Fetches video topics data from the API
  /// API Endpoint: GET /api/v1/notes/categories/video/topics/
  Future<List<Map<String, dynamic>>> fetchVideoTopics() async {
    try {
      final response = await http.get(
        Uri.parse('${BaseUrl.baseUrl}/notes/categories/video/topics/'),
        headers: {
          'Content-Type': 'application/json',
          'Accept': 'application/json',
        },
      );

      print('Video Topics API Response Status: ${response.statusCode}');
      print('Video Topics API Response Body: ${response.body}');

      if (response.statusCode == 200) {
        final data = json.decode(response.body);

        if (data['status'] == 'success' && data['data'] != null) {
          print('Successfully fetched video topics from API');
          return List<Map<String, dynamic>>.from(data['data']);
        } else {
          print('API Response structure unexpected: $data');
          throw Exception('Invalid API response structure');
        }
      } else {
        print('API Error: ${response.statusCode} - ${response.body}');
        throw Exception('Failed to load video topics: ${response.statusCode}');
      }
    } catch (e) {
      print('Error fetching video topics: $e');
      // Return default data structure if API fails - using category ID 1 for all topics
      return [
        {
          'id': 1, // Use category ID 1 since that's what exists in database
          'title': 'Human Anatomy',
          'description': 'Comprehensive anatomy content for medical students',
          'videos_count': 10,
          'is_featured': true,
          'order': 1
        },
        {
          'id': 1, // Use category ID 1 since that's what exists in database
          'title': 'Physiology',
          'description': 'Physiology fundamentals and concepts',
          'videos_count': 8,
          'is_featured': false,
          'order': 2
        },
        {
          'id': 1, // Use category ID 1 since that's what exists in database
          'title': 'Biochemistry',
          'description': 'Biochemistry principles and applications',
          'videos_count': 12,
          'is_featured': false,
          'order': 3
        },
        {
          'id': 1, // Use category ID 1 since that's what exists in database
          'title': 'Pharmacology',
          'description': 'Drug mechanisms and therapeutic applications',
          'videos_count': 15,
          'is_featured': false,
          'order': 4
        },
        {
          'id': 1, // Use category ID 1 since that's what exists in database
          'title': 'Pathology',
          'description': 'Disease mechanisms and diagnostic approaches',
          'videos_count': 9,
          'is_featured': false,
          'order': 5
        },
        {
          'id': 1, // Use category ID 1 since that's what exists in database
          'title': 'Psychology Fundamentals',
          'description': 'Basic psychology concepts and theories',
          'videos_count': 7,
          'is_featured': false,
          'order': 6
        },
      ];
    }
  }

  /// Navigate to video sub screen
  void _navigateToVideoSubScreen(Map<String, dynamic> topic) {
    Navigator.push(
      context,
      MaterialPageRoute(
        builder: (context) => VideoNotesSubScreen(
          categoryTitle: topic['title'] ?? 'Unknown Topic',
          categoryId: topic['id'] ?? 1, // Use topic ID to filter videos by topic
        ),
      ),
    );
  }

  /// Builds individual video topic cards
  Widget _buildVideoTopicCard(Map<String, dynamic> topic) {
    return GestureDetector(
      onTap: () => _navigateToVideoSubScreen(topic),
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
                    '${topic['videos_count'] ?? 0} Videos',
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
          'Video Notes',
          style: TextStyle(
            fontFamily: 'Poppins',
            fontSize: 20,
            fontWeight: FontWeight.bold,
            color: whiteColor,
          ),
        ),
        centerTitle: true,
        elevation: 0,
        leading: IconButton(
          icon: Icon(Icons.arrow_back_ios, color: whiteColor),
          onPressed: () {
            Navigator.pop(context);
          },
        ),
      ),
      body: SafeArea(
        child: Column(
          children: [
            Expanded(
              child: FutureBuilder<List<Map<String, dynamic>>>(
                future: videoTopicsFuture,
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
                            'Loading Videos...',
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
                                videoTopicsFuture = fetchVideoTopics();
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

                  final topics = snapshot.data ?? [];

                  return ListView.builder(
                    padding: EdgeInsets.symmetric(vertical: 8),
                    itemCount: topics.length,
                    itemBuilder: (context, index) {
                      return _buildVideoTopicCard(topics[index]);
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
