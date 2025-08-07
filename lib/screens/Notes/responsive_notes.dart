import 'dart:convert';
import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;
import 'package:frontend/utils/colors/colors.dart';
import 'package:frontend/_env/env.dart';
import 'package:frontend/widgets/botttom_nav.dart';

class ResponsiveNotesSection extends StatefulWidget {
  const ResponsiveNotesSection({super.key});

  @override
  _ResponsiveNotesSectionState createState() => _ResponsiveNotesSectionState();
}

class _ResponsiveNotesSectionState extends State<ResponsiveNotesSection> {
  late Future<Map<String, dynamic>> notesDataFuture;
  int _selectedIndex = 3;

  @override
  void initState() {
    super.initState();
    notesDataFuture = fetchNotesData();
  }

  Future<Map<String, dynamic>> fetchNotesData() async {
    try {
      final response = await http.get(
        Uri.parse('${BaseUrl.baseUrl}/notes/categories/'),
        headers: {
          'Content-Type': 'application/json',
          'Accept': 'application/json',
        },
      );

      print('Responsive Notes API Response Status: ${response.statusCode}');
      print('Responsive Notes API Response Body: ${response.body}');

      if (response.statusCode == 200) {
        final data = json.decode(response.body);

        // Check if the response has the expected structure
        if (data['status'] == 'success' && data['data'] != null) {
          print('Successfully fetched responsive notes data from API');
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
      print('Error fetching responsive notes data: $e');
      return {
        'video': {'topics': 0, 'videos': 0},
        'mcq': {'topics': 0, 'modules': 0},
        'clinical_case': {'topics': 0, 'modules': 0},
        'q_bank': {'topics': 0, 'modules': 0},
        'flash_card': {'topics': 0, 'modules': 0},
      };
    }
  }

  String _formatCount(dynamic count) {
    if (count == null || count == '') return '-';
    if (count == 0) return '0';
    return count.toString();
  }

  Widget _buildContentCard({
    required String title,
    required String topicsCount,
    required String modulesCount,
    required String modulesLabel,
    required BuildContext context,
  }) {
    final screenWidth = MediaQuery.of(context).size.width;
    final isTablet = screenWidth > 600;

    return Container(
      margin: EdgeInsets.symmetric(
          horizontal: isTablet ? 40 : 20, vertical: isTablet ? 12 : 8),
      decoration: BoxDecoration(
        color: whiteColor,
        borderRadius: BorderRadius.circular(isTablet ? 16 : 12),
        boxShadow: [
          BoxShadow(
            color: Colors.black.withOpacity(0.05),
            blurRadius: isTablet ? 15 : 10,
            offset: Offset(0, isTablet ? 3 : 2),
          ),
        ],
      ),
      child: Padding(
        padding: EdgeInsets.all(isTablet ? 28 : 20),
        child: Column(
          children: [
            Row(
              children: [
                Expanded(
                  child: Column(
                    crossAxisAlignment: CrossAxisAlignment.start,
                    children: [
                      Text(
                        title,
                        style: TextStyle(
                          fontFamily: 'Poppins',
                          fontSize: isTablet ? 22 : 18,
                          fontWeight: FontWeight.w600,
                          color: titlecolor,
                        ),
                      ),
                      SizedBox(height: isTablet ? 6 : 4),
                      Text(
                        '$topicsCount Topics',
                        style: TextStyle(
                          fontFamily: 'Poppins',
                          fontSize: isTablet ? 16 : 14,
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
                        fontSize: isTablet ? 14 : 12,
                        color: primaryColor,
                        fontWeight: FontWeight.w500,
                      ),
                    ),
                    SizedBox(width: isTablet ? 12 : 8),
                    Icon(
                      Icons.more_vert,
                      color: grey3,
                      size: isTablet ? 24 : 20,
                    ),
                  ],
                ),
              ],
            ),
          ],
        ),
      ),
    );
  }

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
          _buildNavItem(0, Icons.person_outline, 'Profile', context),
          _buildNavItem(1, Icons.diamond_outlined, 'Diamond', context),
          _buildNavItem(2, Icons.text_fields, 'Y', context),
          _buildNavItem(3, Icons.book, 'Notes', context, isActive: true),
          _buildNavItem(4, Icons.flight, 'Travel', context),
        ],
      ),
    );
  }

  Widget _buildNavItem(
      int index, IconData icon, String label, BuildContext context,
      {bool isActive = false}) {
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
          Icon(
            icon,
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
      backgroundColor: color3,
      appBar: AppBar(
        title: Text(
          'Notes',
          style: TextStyle(
            fontFamily: 'Poppins',
            fontSize: isTablet ? 20 : 18,
            fontWeight: FontWeight.w600,
            color: whiteColor,
          ),
        ),
        backgroundColor: primaryColor,
        elevation: 0,
        leading: IconButton(
          icon: Icon(Icons.menu, color: whiteColor),
          onPressed: () {
            // TODO: Implement drawer navigation
          },
        ),
        actions: [
          IconButton(
            icon: Icon(Icons.search, color: whiteColor),
            onPressed: () {
              // TODO: Implement search functionality
            },
          ),
          IconButton(
            icon: Icon(Icons.notifications, color: whiteColor),
            onPressed: () {
              // TODO: Implement notifications functionality
            },
          ),
        ],
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
                            strokeWidth: isTablet ? 4 : 2,
                          ),
                          SizedBox(height: isTablet ? 24 : 16),
                          Text(
                            'Loading Notes...',
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
                                fontSize: isTablet ? 16 : 14,
                              ),
                            ),
                          ),
                        ],
                      ),
                    );
                  }

                  final data = snapshot.data ?? {};

                  // For landscape tablets, show cards in a grid
                  if (isTablet && isLandscape) {
                    return GridView.builder(
                      padding:
                          EdgeInsets.symmetric(horizontal: 20, vertical: 10),
                      gridDelegate: SliverGridDelegateWithFixedCrossAxisCount(
                        crossAxisCount: 2,
                        childAspectRatio: 2.5,
                        crossAxisSpacing: 20,
                        mainAxisSpacing: 20,
                      ),
                      itemCount: 5,
                      itemBuilder: (context, index) {
                        final categories = [
                          {'title': 'Video', 'key': 'video', 'label': 'Videos'},
                          {'title': 'MCQ', 'key': 'mcq', 'label': 'Modules'},
                          {
                            'title': 'Clinical Case',
                            'key': 'clinical_case',
                            'label': 'Modules'
                          },
                          {
                            'title': 'Q-Bank',
                            'key': 'q_bank',
                            'label': 'Modules'
                          },
                          {
                            'title': 'Flash Card',
                            'key': 'flash_card',
                            'label': 'Modules'
                          },
                        ];

                        final category = categories[index];
                        return _buildContentCard(
                          title: category['title']!,
                          topicsCount:
                              _formatCount(data[category['key']]?['topics']),
                          modulesCount: _formatCount(data[category['key']]
                                  ?['modules'] ??
                              data[category['key']]?['videos']),
                          modulesLabel: category['label']!,
                          context: context,
                        );
                      },
                    );
                  }

                  // For portrait and mobile, show cards in a list
                  return ListView(
                    padding: EdgeInsets.symmetric(vertical: 10),
                    children: [
                      _buildContentCard(
                        title: 'Video',
                        topicsCount: _formatCount(data['video']?['topics']),
                        modulesCount: _formatCount(data['video']?['videos']),
                        modulesLabel: 'Videos',
                        context: context,
                      ),
                      _buildContentCard(
                        title: 'MCQ',
                        topicsCount: _formatCount(data['mcq']?['topics']),
                        modulesCount: _formatCount(data['mcq']?['modules']),
                        modulesLabel: 'Modules',
                        context: context,
                      ),
                      _buildContentCard(
                        title: 'Clinical Case',
                        topicsCount:
                            _formatCount(data['clinical_case']?['topics']),
                        modulesCount:
                            _formatCount(data['clinical_case']?['modules']),
                        modulesLabel: 'Modules',
                        context: context,
                      ),
                      _buildContentCard(
                        title: 'Q-Bank',
                        topicsCount: _formatCount(data['q_bank']?['topics']),
                        modulesCount: _formatCount(data['q_bank']?['modules']),
                        modulesLabel: 'Modules',
                        context: context,
                      ),
                      _buildContentCard(
                        title: 'Flash Card',
                        topicsCount:
                            _formatCount(data['flash_card']?['topics']),
                        modulesCount:
                            _formatCount(data['flash_card']?['modules']),
                        modulesLabel: 'Modules',
                        context: context,
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
