import 'dart:convert';
import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;
import 'package:notes/utils/colors/colors.dart';
import 'package:notes/_env/env.dart';

class ResponsiveQBankNotesScreen extends StatefulWidget {
  const ResponsiveQBankNotesScreen({super.key});

  @override
  _ResponsiveQBankNotesScreenState createState() =>
      _ResponsiveQBankNotesScreenState();
}

class _ResponsiveQBankNotesScreenState
    extends State<ResponsiveQBankNotesScreen> {
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

      print(
        'Responsive Q-Bank Topics API Response Status: ${response.statusCode}',
      );
      print('Responsive Q-Bank Topics API Response Body: ${response.body}');

      if (response.statusCode == 200) {
        final data = json.decode(response.body);

        if (data['status'] == 'success' && data['data'] != null) {
          print('Successfully fetched responsive Q-Bank topics from API');
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
      print('Error fetching responsive Q-Bank topics: $e');
      // Return default data structure if API fails
      return [
        {
          'id': 1,
          'title': 'Anatomy Q-Bank',
          'description':
              'Comprehensive anatomy question bank for medical students',
          'modules_count': 18,
          'is_featured': true,
          'order': 1,
        },
        {
          'id': 2,
          'title': 'Physiology Q-Bank',
          'description': 'Physiology question bank and practice questions',
          'modules_count': 15,
          'is_featured': false,
          'order': 2,
        },
        {
          'id': 3,
          'title': 'Biochemistry Q-Bank',
          'description': 'Biochemistry question bank and molecular concepts',
          'modules_count': 20,
          'is_featured': false,
          'order': 3,
        },
        {
          'id': 4,
          'title': 'Pharmacology Q-Bank',
          'description': 'Drug mechanisms and therapeutic question bank',
          'modules_count': 22,
          'is_featured': false,
          'order': 4,
        },
        {
          'id': 5,
          'title': 'Pathology Q-Bank',
          'description': 'Disease mechanisms and diagnostic question bank',
          'modules_count': 16,
          'is_featured': false,
          'order': 5,
        },
        {
          'id': 6,
          'title': 'Microbiology Q-Bank',
          'description':
              'Microbial organisms and infectious disease question bank',
          'modules_count': 19,
          'is_featured': false,
          'order': 6,
        },
        {
          'id': 7,
          'title': 'Forensic Medicine Q-Bank',
          'description': 'Forensic science and toxicological question bank',
          'modules_count': 12,
          'is_featured': false,
          'order': 7,
        },
        {
          'id': 8,
          'title': 'Community Medicine Q-Bank',
          'description': 'Public health and community healthcare question bank',
          'modules_count': 14,
          'is_featured': false,
          'order': 8,
        },
      ];
    }
  }

  /// Builds individual Q-Bank topic cards
  Widget _buildQBankTopicCard(
    Map<String, dynamic> topic,
    BuildContext context,
  ) {
    final screenWidth = MediaQuery.of(context).size.width;
    final isTablet = screenWidth > 600;

    return Container(
      margin: EdgeInsets.symmetric(
        horizontal: isTablet ? 40 : 20,
        vertical: isTablet ? 8 : 4,
      ),
      decoration: BoxDecoration(
        color: whiteColor,
        borderRadius: BorderRadius.circular(isTablet ? 12 : 8),
        border: Border(bottom: BorderSide(color: grey1, width: 1)),
        boxShadow: isTablet
            ? [
                BoxShadow(
                  color: Colors.black.withOpacity(0.05),
                  blurRadius: 10,
                  offset: Offset(0, 2),
                ),
              ]
            : null,
      ),
      child: Padding(
        padding: EdgeInsets.symmetric(
          horizontal: isTablet ? 24 : 16,
          vertical: isTablet ? 16 : 12,
        ),
        child: Row(
          children: [
            Expanded(
              child: Text(
                topic['title'] ?? 'Unknown Topic',
                style: TextStyle(
                  fontFamily: 'Poppins',
                  fontSize: isTablet ? 20 : 16,
                  fontWeight: FontWeight.w500,
                  color: titlecolor,
                ),
              ),
            ),
            Text(
              '${topic['modules_count'] ?? 0} Modules',
              style: TextStyle(
                fontFamily: 'Poppins',
                fontSize: isTablet ? 16 : 14,
                color: grey3,
              ),
            ),
          ],
        ),
      ),
    );
  }

  /// Builds bottom navigation bar
  Widget _buildBottomNavigation(BuildContext context) {
    final screenWidth = MediaQuery.of(context).size.width;
    final isTablet = screenWidth > 600;

    return Container(
      height: isTablet ? 100 : 80,
      decoration: BoxDecoration(
        color: primaryColor,
        borderRadius: BorderRadius.only(
          topLeft: Radius.circular(isTablet ? 25 : 20),
          topRight: Radius.circular(isTablet ? 25 : 20),
        ),
      ),
      child: Row(
        mainAxisAlignment: MainAxisAlignment.spaceEvenly,
        children: [
          _buildNavItem(0, 'assets/frame.png', 'Profile', context),
          _buildNavItem(1, 'assets/diamonds.png', 'Diamond', context),
          _buildNavItem(2, 'assets/Group 98.png', 'Y', context),
          _buildNavItem(3, 'assets/book.png', 'Notes', context, isActive: true),
          _buildNavItem(4, 'assets/airplane.png', 'Travel', context),
        ],
      ),
    );
  }

  /// Builds individual navigation items
  Widget _buildNavItem(
    int index,
    String iconPath,
    String label,
    BuildContext context, {
    bool isActive = false,
  }) {
    final screenWidth = MediaQuery.of(context).size.width;
    final isTablet = screenWidth > 600;

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
            size: isTablet ? 28 : 24,
          ),
          if (isActive)
            Container(
              margin: EdgeInsets.only(top: isTablet ? 6 : 4),
              height: isTablet ? 3 : 2,
              width: isTablet ? 25 : 20,
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
    final screenWidth = MediaQuery.of(context).size.width;
    final screenHeight = MediaQuery.of(context).size.height;
    final isTablet = screenWidth > 600;
    final isLandscape = screenWidth > screenHeight;

    return Scaffold(
      appBar: AppBar(
        title: Text(
          'Q-Bank Topics',
          style: TextStyle(
            fontFamily: 'Poppins',
            fontSize: isTablet ? 20 : 16,
            color: whiteColor,
          ),
        ),
        backgroundColor: primaryColor,
        elevation: 0,
        centerTitle: true,
        leading: IconButton(
          icon: Icon(Icons.arrow_back_ios, color: whiteColor),
          onPressed: () {
            Navigator.pop(context);
          },
        ),
      ),
      backgroundColor: color3,
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
                            strokeWidth: isTablet ? 4 : 2,
                          ),
                          SizedBox(height: isTablet ? 24 : 16),
                          Text(
                            'Loading Q-Bank...',
                            style: TextStyle(
                              fontFamily: 'Poppins',
                              fontSize: isTablet ? 20 : 16,
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
                            size: isTablet ? 64 : 48,
                            color: grey3,
                          ),
                          SizedBox(height: isTablet ? 24 : 16),
                          Text(
                            'Failed to load content',
                            style: TextStyle(
                              fontFamily: 'Poppins',
                              fontSize: isTablet ? 20 : 16,
                              color: grey3,
                            ),
                          ),
                          SizedBox(height: isTablet ? 12 : 8),
                          Text(
                            'Please check your connection',
                            style: TextStyle(
                              fontFamily: 'Poppins',
                              fontSize: isTablet ? 16 : 14,
                              color: grey3,
                            ),
                          ),
                          SizedBox(height: isTablet ? 24 : 16),
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
                                fontSize: isTablet ? 16 : 14,
                              ),
                            ),
                          ),
                        ],
                      ),
                    );
                  }

                  final topics = snapshot.data ?? [];

                  // For landscape tablets, show cards in a grid
                  if (isTablet && isLandscape) {
                    return GridView.builder(
                      padding: EdgeInsets.symmetric(
                        horizontal: 20,
                        vertical: 10,
                      ),
                      gridDelegate: SliverGridDelegateWithFixedCrossAxisCount(
                        crossAxisCount: 2,
                        childAspectRatio: 3.0,
                        crossAxisSpacing: 20,
                        mainAxisSpacing: 20,
                      ),
                      itemCount: topics.length,
                      itemBuilder: (context, index) {
                        return _buildQBankTopicCard(topics[index], context);
                      },
                    );
                  }

                  // For portrait and mobile, show cards in a list
                  return ListView.builder(
                    padding: EdgeInsets.symmetric(vertical: 8),
                    itemCount: topics.length,
                    itemBuilder: (context, index) {
                      return _buildQBankTopicCard(topics[index], context);
                    },
                  );
                },
              ),
            ),
          ],
        ),
      ),
    );
  }
}
