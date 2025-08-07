import 'dart:convert';
import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;
import 'package:frontend/utils/colors/colors.dart';
import 'package:frontend/_env/env.dart';
import 'package:frontend/widgets/botttom_nav.dart';

class QuestionBankNotesScreen extends StatefulWidget {
  const QuestionBankNotesScreen({super.key});

  @override
  _QuestionBankNotesScreenState createState() =>
      _QuestionBankNotesScreenState();
}

class _QuestionBankNotesScreenState extends State<QuestionBankNotesScreen> {
  late Future<List<Map<String, dynamic>>> qBankTopicsFuture;
  int _selectedIndex = 3; // Notes tab is active

  @override
  void initState() {
    super.initState();
    qBankTopicsFuture = fetchQBankTopics();
  }

  /// Fetches Q-Bank topics data from the API
  /// API Endpoint: GET /api/v1/notes/categories/q_bank/topics/
  Future<List<Map<String, dynamic>>> fetchQBankTopics() async {
    try {
      final response = await http.get(
        Uri.parse('${BaseUrl.baseUrl}/notes/categories/q_bank/topics/'),
        headers: {
          'Content-Type': 'application/json',
          'Accept': 'application/json',
        },
      );

      print('Q-Bank Topics API Response Status: ${response.statusCode}');
      print('Q-Bank Topics API Response Body: ${response.body}');

      if (response.statusCode == 200) {
        final data = json.decode(response.body);

        if (data['status'] == 'success' && data['data'] != null) {
          print('Successfully fetched Q-Bank topics from API');
          return List<Map<String, dynamic>>.from(data['data']);
        } else {
          print('API Response structure unexpected: $data');
          throw Exception('Invalid API response structure');
        }
      } else {
        print('API Error: ${response.statusCode} - ${response.body}');
        throw Exception('Failed to load Q-Bank topics: ${response.statusCode}');
      }
    } catch (e) {
      print('Error fetching Q-Bank topics: $e');
      // Return default data structure if API fails
      return [
        {
          'id': 1,
          'title': 'Anatomy Q-Bank',
          'description':
              'Comprehensive anatomy question bank for medical students',
          'modules_count': 18,
          'is_featured': true,
          'order': 1
        },
        {
          'id': 2,
          'title': 'Physiology Q-Bank',
          'description': 'Physiology question bank and practice questions',
          'modules_count': 15,
          'is_featured': false,
          'order': 2
        },
        {
          'id': 3,
          'title': 'Biochemistry Q-Bank',
          'description': 'Biochemistry question bank and molecular concepts',
          'modules_count': 20,
          'is_featured': false,
          'order': 3
        },
        {
          'id': 4,
          'title': 'Pharmacology Q-Bank',
          'description': 'Drug mechanisms and therapeutic question bank',
          'modules_count': 22,
          'is_featured': false,
          'order': 4
        },
        {
          'id': 5,
          'title': 'Pathology Q-Bank',
          'description': 'Disease mechanisms and diagnostic question bank',
          'modules_count': 16,
          'is_featured': false,
          'order': 5
        },
        {
          'id': 6,
          'title': 'Microbiology Q-Bank',
          'description':
              'Microbial organisms and infectious disease question bank',
          'modules_count': 19,
          'is_featured': false,
          'order': 6
        },
        {
          'id': 7,
          'title': 'Forensic Medicine Q-Bank',
          'description': 'Forensic science and toxicological question bank',
          'modules_count': 12,
          'is_featured': false,
          'order': 7
        },
        {
          'id': 8,
          'title': 'Community Medicine Q-Bank',
          'description': 'Public health and community healthcare question bank',
          'modules_count': 14,
          'is_featured': false,
          'order': 8
        },
      ];
    }
  }

  /// Builds individual Q-Bank topic cards
  Widget _buildQBankTopicCard(Map<String, dynamic> topic) {
    return Container(
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
            Text(
              '${topic['modules_count'] ?? 0} Modules',
              style: TextStyle(
                fontFamily: 'Poppins',
                fontSize: 14,
                color: grey3,
              ),
            ),
          ],
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
          'Q-Bank Notes',
          style: TextStyle(
            fontFamily: 'Poppins',
            fontSize: 20,
            fontWeight: FontWeight.w600,
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
                future: qBankTopicsFuture,
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
                            'Loading Q-Bank...',
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
                                qBankTopicsFuture = fetchQBankTopics();
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
                      return _buildQBankTopicCard(topics[index]);
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
