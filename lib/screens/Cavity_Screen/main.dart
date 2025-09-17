import 'dart:convert';
import 'package:flutter/material.dart';
import 'package:frontend/utils/colors/colors.dart';
import 'package:frontend/services/cavity_api_service.dart';
import 'package:frontend/utils/session_manager.dart';

class CavityScreen extends StatefulWidget {
  const CavityScreen({super.key});

  @override
  _CavityScreenState createState() => _CavityScreenState();
}

class _CavityScreenState extends State<CavityScreen> {
  List<Map<String, dynamic>> allPosts = []; // List for posts from API
  String selectedYear = 'NEET UG 2025'; // Fixed to match backend format
  bool isDropdownOpen = false;
  bool isLoading = true;

  // State variables
  Map<int, bool> postComments = {}; // Track comment box state for each post
  Map<int, String> postCommentTexts = {}; // Track comment text for each post
  Map<int, bool> postShares = {}; // Track share options state for each post

  // Share platform definitions
  final Map<String, Map<String, dynamic>> sharePlatforms = {
    'LinkedIn': {
      'color': Color.fromARGB(255, 0, 0, 0),
      'icon': Icons.work,
      'text': 'LinkedIn',
    },
    'WhatsApp': {
      'color': Color.fromARGB(255, 0, 0, 0),
      'icon': Icons.chat,
      'text': 'WhatsApp',
    },
    'Facebook': {
      'color': Color.fromARGB(255, 0, 0, 0),
      'icon': Icons.facebook,
      'text': 'Facebook',
    },
    'Instagram': {
      'color': Color.fromARGB(255, 0, 0, 0),
      'icon': Icons.camera_alt,
      'text': 'Instagram',
    },
    'Email': {
      'color': Color.fromARGB(255, 0, 0, 0),
      'icon': Icons.email,
      'text': 'Email',
    },
    'Snapchat': {
      'color': Color.fromARGB(255, 0, 0, 0),
      'icon': Icons.camera_alt,
      'text': 'Snapchat',
    },
    'SMS': {
      'color': Color.fromARGB(255, 0, 0, 0),
      'icon': Icons.sms,
      'text': 'SMS',
    },
    'Bluetooth': {
      'color': Color.fromARGB(255, 0, 0, 0),
      'icon': Icons.bluetooth,
      'text': 'Bluetooth',
    },
  };

  final List<String> availableYears = [
    'NEET UG 2025',
    'NEET UG 2024',
    'NEET UG 2023',
    'NEET PG 2025',
    'NEET PG 2024',
    'NEET PG 2023',
    'MBBS 1st Year',
    'MBBS 2nd Year',
    'MBBS 3rd Year',
    'MBBS 4th Year',
    'MBBS (House Surgeon)',
    'MBBS PG 1st year',
    'MBBS PG 2nd Year',
  ];

  @override
  void initState() {
    super.initState();
    _testApiConnection();
    _loadData();
  }

  /// Test API connection
  Future<void> _testApiConnection() async {
    print('🔍 DEBUG: Testing API connection...');
    bool isConnected = await CavityApiService.testApiConnection();
    print('🔍 DEBUG: API connection test result: $isConnected');
  }

  /// Load data from API
  Future<void> _loadData() async {
    print('🔍 DEfgfgfgfgfgBUG: Starting _loadData method');
    print('🔍 DEBUG: Selected year: $selectedYear');

    try {
      print('🔍 DEBUG: Setting loading state to true');
      setState(() {
        isLoading = true;
      });

      print('🔍 DEBUG: About to call CavityApiService.getPostsByYear');
      // Load posts from API
      List<Map<String, dynamic>> apiPosts =
          await CavityApiService.getPostsByYear(selectedYear);

      print('🔍 DEBUG: API call completed');
      print('🔍 DEBUG: Received ${apiPosts.length} posts from API');
      print('🔍 DEBUG: Posts data: $apiPosts');

      print('🔍 DEBUG: About to update state with posts');
      setState(() {
        allPosts = apiPosts;
        isLoading = false;
      });
      print('🔍 DEBUG: State updated, allPosts length: ${allPosts.length}');
      print('🔍 DEBUG: isLoading set to false');
    } catch (e) {
      print('❌ ERROR in _loadData: $e');
      print('❌ ERROR type: ${e.runtimeType}');
      setState(() {
        isLoading = false;
        allPosts = []; // Empty list if API fails
      });
      print('🔍 DEBUG: Error state set, allPosts length: ${allPosts.length}');
    }
  }

  /// Change selected year and filter posts
  void _changeYear(String newYear) {
    print('🔍 DEBUG: Changing year from $selectedYear to $newYear');
    setState(() {
      selectedYear = newYear;
      isDropdownOpen = false;
    });
    print('🔍 DEBUG: Year changed to $selectedYear, dropdown closed');
    _loadData(); // Reload data when year changes
  }

  /// Format timestamp for display
  String _formatTimestamp(DateTime dateTime) {
    DateTime now = DateTime.now();
    Duration difference = now.difference(dateTime);

    if (difference.inDays > 0) {
      return '${dateTime.day} ${_getMonthName(dateTime.month)} at ${_formatTime(dateTime)}';
    } else if (difference.inHours > 0) {
      return '${difference.inHours}h ago';
    } else if (difference.inMinutes > 0) {
      return '${difference.inMinutes}m ago';
    } else {
      return 'Just now';
    }
  }

  /// Get month name
  String _getMonthName(int month) {
    List<String> months = [
      'Jan',
      'Feb',
      'Mar',
      'Apr',
      'May',
      'Jun',
      'Jul',
      'Aug',
      'Sep',
      'Oct',
      'Nov',
      'Dec'
    ];
    return months[month - 1];
  }

  /// Format time
  String _formatTime(DateTime dateTime) {
    int hour = dateTime.hour;
    String period = hour < 12 ? 'AM' : 'PM';
    if (hour == 0) hour = 12;
    if (hour > 12) hour -= 12;
    return '$hour:${dateTime.minute.toString().padLeft(2, '0')} $period';
  }

  /// Toggle like for a post
  void _toggleLike(int postIndex) async {
    print('🔍 DEBUG: _toggleLike called for post index: $postIndex');
    if (postIndex < allPosts.length) {
      Map<String, dynamic> post = allPosts[postIndex];
      String postId = post['id']?.toString() ?? '';
      print('🔍 DEBUG: Post ID: $postId');

      if (postId.isNotEmpty) {
        bool isLiked = post['is_liked_by_user'] ?? false;
        print('🔍 DEBUG: Current is_liked_by_user: $isLiked');
        bool success = false;
        Map<String, dynamic>? responseData;

        if (isLiked) {
          // Unlike
          print('🔍 DEBUG: Attempting to unlike post');
          responseData = await CavityApiService.unlikePostWithResponse(postId);
          success = responseData != null;
        } else {
          // Like
          print('🔍 DEBUG: Attempting to like post');
          responseData = await CavityApiService.likePostWithResponse(postId);
          success = responseData != null;
        }

        print('🔍 DEBUG: API call success: $success');
        print('🔍 DEBUG: Response data: $responseData');

        if (success && responseData != null) {
          // Update the post data immediately with response data
          setState(() {
            allPosts[postIndex]['is_liked_by_user'] =
                responseData!['is_liked'] ?? !isLiked;
            allPosts[postIndex]['like_count'] =
                responseData!['like_count'] ?? post['like_count'];
          });
          print('🔍 DEBUG: Updated post data immediately');
        } else {
          // Show error message
          ScaffoldMessenger.of(context).showSnackBar(
            SnackBar(
              content: Text('Failed to ${isLiked ? 'unlike' : 'like'} post'),
              backgroundColor: Colors.red,
            ),
          );
        }
      }
    }
  }

  /// Toggle comment box for a post
  void _toggleComment(int postIndex) {
    setState(() {
      postComments[postIndex] = !(postComments[postIndex] ?? false);
      if (!(postComments[postIndex] ?? false)) {
        postCommentTexts[postIndex] = ''; // Clear comment text when closing
      }
    });
  }

  /// Update comment text for a post
  void _updateCommentText(int postIndex, String text) {
    setState(() {
      postCommentTexts[postIndex] = text;
    });
  }

  /// Submit comment for a post
  void _submitComment(int postIndex) async {
    String comment = postCommentTexts[postIndex] ?? '';
    if (comment.trim().isNotEmpty) {
      if (postIndex < allPosts.length) {
        Map<String, dynamic> post = allPosts[postIndex];
        String postId = post['id']?.toString() ?? '';
        String email = await SessionManager.getStoredEmail() ?? '';
        if (postId.isNotEmpty) {
          bool success =
              await CavityApiService.addComment(postId, comment, email);

          if (success) {
            setState(() {
              postCommentTexts[postIndex] = '';
              postComments[postIndex] = false; // Close comment box
            });
            // Refresh the data to get updated comment count from backend
            _loadData();
            ScaffoldMessenger.of(context).showSnackBar(
              SnackBar(
                content: Text('Comment posted successfully!'),
                backgroundColor: primaryColor,
              ),
            );
          } else {
            ScaffoldMessenger.of(context).showSnackBar(
              SnackBar(
                content: Text('Failed to post comment'),
                backgroundColor: Colors.red,
              ),
            );
          }
        }
      }
    }
  }

  /// Show share options for a post
  void _showShareOptions(int postIndex) {
    setState(() {
      postShares[postIndex] = !(postShares[postIndex] ?? false);
    });
  }

  /// Share to specific platform
  void _shareToPlatform(String platform, int postIndex) async {
    if (postIndex < allPosts.length) {
      Map<String, dynamic> post = allPosts[postIndex];
      String postId = post['id']?.toString() ?? '';

      if (postId.isNotEmpty) {
        bool success = await CavityApiService.sharePost(postId, platform);

        setState(() {
          postShares[postIndex] = false; // Close share sheet
        });

        if (success) {
          ScaffoldMessenger.of(context).showSnackBar(
            SnackBar(
              content: Text('Sharing to $platform...'),
              backgroundColor: primaryColor,
            ),
          );
        } else {
          ScaffoldMessenger.of(context).showSnackBar(
            SnackBar(
              content: Text('Failed to share to $platform'),
              backgroundColor: Colors.red,
            ),
          );
        }
      }
    }
  }

  /// Format comment timestamp
  String _formatCommentTimestamp(String timestamp) {
    try {
      DateTime dateTime = DateTime.parse(timestamp);
      return _formatTimestamp(dateTime);
    } catch (e) {
      print('❌ ERROR parsing comment timestamp: $e');
      return 'Unknown time';
    }
  }

  /// Build the header with app title and year dropdown
  Widget _buildHeader() {
    return Container(
      padding: EdgeInsets.symmetric(horizontal: 20, vertical: 15),
      decoration: BoxDecoration(
        color: whiteColor,
        boxShadow: [
          BoxShadow(
            color: Colors.black.withValues(alpha: 0.05),
            blurRadius: 10,
            offset: Offset(0, 2),
          ),
        ],
      ),
      child: Row(
        mainAxisSize: MainAxisSize.max, // Explicitly set max size
        children: [
          // App Title
          Text(
            'Cavity',
            style: TextStyle(
              fontFamily: 'Poppins',
              fontSize: 24,
              fontWeight: FontWeight.w700,
              color: titlecolor,
            ),
          ),
          Spacer(),
          // Year Dropdown
          GestureDetector(
            onTap: () {
              print(
                  '🔍 DEBUG: Dropdown tapped, current state: $isDropdownOpen');
              setState(() {
                isDropdownOpen = !isDropdownOpen;
              });
              print('🔍 DEBUG: Dropdown state changed to: $isDropdownOpen');
            },
            child: Container(
              padding: EdgeInsets.symmetric(horizontal: 16, vertical: 8),
              decoration: BoxDecoration(
                color: primaryColor.withValues(alpha: 0.1),
                borderRadius: BorderRadius.circular(20),
                border: Border.all(color: primaryColor.withValues(alpha: 0.3)),
              ),
              child: Row(
                mainAxisSize: MainAxisSize.min,
                children: [
                  Text(
                    selectedYear,
                    style: TextStyle(
                      fontFamily: 'Poppins',
                      fontSize: 14,
                      fontWeight: FontWeight.w600,
                      color: primaryColor,
                    ),
                  ),
                  SizedBox(width: 8),
                  AnimatedRotation(
                    turns: isDropdownOpen ? 0.5 : 0,
                    duration: Duration(milliseconds: 200),
                    child: Icon(
                      Icons.keyboard_arrow_down,
                      color: primaryColor,
                      size: 20,
                    ),
                  ),
                ],
              ),
            ),
          ),
        ],
      ),
    );
  }

  /// Build the year selection modal
  Widget _buildYearSelectionModal() {
    if (!isDropdownOpen) return SizedBox.shrink();

    return Positioned(
      top: 80,
      right: 20,
      child: Material(
        color: Colors.transparent,
        child: Container(
          width: 200, // Fixed width to prevent unbounded constraints
          constraints: BoxConstraints(
            maxHeight: 350, // Increased max height
            minHeight: 100, // Minimum height
          ),
          decoration: BoxDecoration(
            color: whiteColor,
            borderRadius: BorderRadius.circular(12),
            boxShadow: [
              BoxShadow(
                color: Colors.black.withValues(alpha: 0.1),
                blurRadius: 10,
                offset: Offset(0, 4),
              ),
            ],
          ),
          child: Column(
            mainAxisSize: MainAxisSize.min,
            children: [
              // Modal Header
              Container(
                padding: EdgeInsets.all(16),
                decoration: BoxDecoration(
                  color: primaryColor.withValues(alpha: 0.1),
                  borderRadius: BorderRadius.only(
                    topLeft: Radius.circular(12),
                    topRight: Radius.circular(12),
                  ),
                ),
                child: Row(
                  mainAxisSize: MainAxisSize.min, // Prevent expansion
                  children: [
                    Icon(Icons.filter_list, color: primaryColor, size: 20),
                    SizedBox(width: 8),
                    Expanded(
                      // Wrap text in Expanded
                      child: Text(
                        'Select Year',
                        style: TextStyle(
                          fontFamily: 'Poppins',
                          fontSize: 16,
                          fontWeight: FontWeight.w600,
                          color: primaryColor,
                        ),
                      ),
                    ),
                  ],
                ),
              ),
              // Year Options - Scrollable
              Expanded(
                child: SingleChildScrollView(
                  child: Column(
                    mainAxisSize: MainAxisSize.min,
                    children: availableYears
                        .map((year) => _buildYearOption(year))
                        .toList(),
                  ),
                ),
              ),
            ],
          ),
        ),
      ),
    );
  }

  /// Build individual year option
  Widget _buildYearOption(String year) {
    final isSelected = year == selectedYear;

    return Material(
      color: Colors.transparent,
      child: InkWell(
        onTap: () => _changeYear(year),
        child: Container(
          padding: EdgeInsets.symmetric(
              horizontal: 16, vertical: 10), // Reduced vertical padding
          decoration: BoxDecoration(
            color: isSelected
                ? primaryColor.withValues(alpha: 0.1)
                : Colors.transparent,
            border: Border(
              bottom: BorderSide(
                color: grey1.withValues(alpha: 0.3),
                width: 0.5,
              ),
            ),
          ),
          child: Row(
            mainAxisSize: MainAxisSize.min, // Prevent expansion
            children: [
              Flexible(
                // Use Flexible instead of Expanded
                child: Text(
                  year,
                  style: TextStyle(
                    fontFamily: 'Poppins',
                    fontSize: 13, // Slightly smaller font
                    fontWeight: isSelected ? FontWeight.w600 : FontWeight.w400,
                    color: isSelected ? primaryColor : titlecolor,
                  ),
                ),
              ),
              if (isSelected)
                Icon(
                  Icons.check,
                  color: primaryColor,
                  size: 16,
                ),
            ],
          ),
        ),
      ),
    );
  }

  /// Build individual post block (Facebook-style)
  Widget _buildPostBlock(Map<String, dynamic> post, int postIndex) {
    // Debug: Print the post data
    print('🔍 DEBUG: Building post block for index $postIndex');
    print('🔍 DEBUG: Post data: $post');

    // Format timestamp from created_at
    String timestamp = '';
    if (post['created_at'] != null) {
      try {
        DateTime dateTime = DateTime.parse(post['created_at']);
        timestamp = _formatTimestamp(dateTime);
      } catch (e) {
        print('❌ ERROR parsing timestamp: $e');
        timestamp = 'Unknown time';
      }
    }

    // Get user information
    Map<String, dynamic>? userData = post['user'];
    String userName = 'Unknown User';
    if (userData != null) {
      userName =
          userData['full_name'] ?? userData['username'] ?? 'Unknown User';
      // userName = userName as String;
      // userName = userName.split('_');
      print('🔍 DEBUG: User data: $userData');
      print('🔍 DEBUG: User name: $userName');
    } else {
      print('⚠️ WARNING: No user data found in post');
    }

    // Get year information
    String year = post['year'] ?? 'Unknown Year';
    print('🔍 DEBUG: Year: $year');

    // Use the is_liked_by_user field from the API response
    bool isLiked = post['is_liked_by_user'] ?? false;
    print('🔍 DEBUG: is_liked_by_user from API: ${post['is_liked_by_user']}');
    print('🔍 DEBUG: isLiked variable: $isLiked');
    bool isCommentOpen = postComments[postIndex] ?? false;
    bool isShareOpen = postShares[postIndex] ?? false;

    return Container(
      margin: EdgeInsets.symmetric(horizontal: 20, vertical: 8),
      decoration: BoxDecoration(
        color: whiteColor,
        borderRadius: BorderRadius.circular(12),
        boxShadow: [
          BoxShadow(
            color: Colors.black.withValues(alpha: 0.05),
            blurRadius: 10,
            offset: Offset(0, 2),
          ),
        ],
      ),
      child: Column(
        children: [
          // Post Header (User Info + Timestamp)
          Padding(
            padding: EdgeInsets.all(16),
            child: Row(
              children: [
                // Profile Image (Red Container)
                Container(
                  width: 40,
                  height: 40,
                  decoration: BoxDecoration(
                    color: Colors.red,
                    borderRadius: BorderRadius.circular(8),
                  ),
                  child: Center(
                    child: Icon(
                      Icons.person,
                      color: whiteColor,
                      size: 20,
                    ),
                  ),
                ),
                SizedBox(width: 12),
                // User Info and Timestamp
                Expanded(
                  child: Column(
                    crossAxisAlignment: CrossAxisAlignment.start,
                    children: [
                      Text(
                        userName,
                        style: TextStyle(
                          fontFamily: 'Poppins',
                          fontSize: 14,
                          fontWeight: FontWeight.w600,
                          color: titlecolor,
                        ),
                      ),
                      SizedBox(height: 2),
                      Row(
                        children: [
                          // Year Tag
                          Container(
                            padding: EdgeInsets.symmetric(
                                horizontal: 6, vertical: 2),
                            decoration: BoxDecoration(
                              color: secondaryColor.withValues(alpha: 0.1),
                              borderRadius: BorderRadius.circular(8),
                            ),
                            child: Text(
                              year,
                              style: TextStyle(
                                fontFamily: 'Poppins',
                                fontSize: 10,
                                fontWeight: FontWeight.w500,
                                color: secondaryColor,
                              ),
                            ),
                          ),
                          SizedBox(width: 8),
                          // Timestamp
                          if (timestamp.isNotEmpty)
                            Text(
                              timestamp,
                              style: TextStyle(
                                fontFamily: 'Poppins',
                                fontSize: 10,
                                color: grey3,
                                fontStyle: FontStyle.italic,
                              ),
                            ),
                        ],
                      ),
                    ],
                  ),
                ),
              ],
            ),
          ),
          // Divider
          Divider(
            color: grey1.withValues(alpha: 0.3),
            height: 1,
          ),
          // Post Content
          Padding(
            padding: EdgeInsets.all(16),
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Text(
                  post['content'] ?? 'No content available',
                  style: TextStyle(
                    fontFamily: 'Poppins',
                    fontSize: 14,
                    height: 1.6,
                    color: titlecolor,
                  ),
                ),
                SizedBox(height: 16),
                // Action Row
                Row(
                  children: [
                    // Like Button
                    GestureDetector(
                      onTap: () => _toggleLike(postIndex),
                      child: Container(
                        padding:
                            EdgeInsets.symmetric(horizontal: 8, vertical: 4),
                        decoration: BoxDecoration(
                          color: (post['like_count'] ?? 0) > 0
                              ? Colors.green.withValues(alpha: 0.1)
                              : Colors.transparent,
                          borderRadius: BorderRadius.circular(12),
                          border: (post['like_count'] ?? 0) > 0
                              ? Border.all(
                                  color: Colors.green.withValues(alpha: 0.3))
                              : null,
                        ),
                        child: Row(
                          children: [
                            Icon(
                              isLiked ? Icons.favorite : Icons.favorite_border,
                              color: (post['like_count'] ?? 0) > 0
                                  ? Colors.green
                                  : (isLiked ? primaryColor : grey3),
                              size: 20,
                            ),
                            SizedBox(width: 8),
                            Text(
                              '${post['like_count'] ?? 0}',
                              style: TextStyle(
                                fontFamily: 'Poppins',
                                fontSize: 12,
                                color: (post['like_count'] ?? 0) > 0
                                    ? Colors.green
                                    : (isLiked ? primaryColor : grey3),
                              ),
                            ),
                          ],
                        ),
                      ),
                    ),
                    SizedBox(width: 16),
                    // Comment Button
                    GestureDetector(
                      onTap: () => _toggleComment(postIndex),
                      child: Row(
                        children: [
                          Icon(
                            isCommentOpen
                                ? Icons.comment
                                : Icons.comment_outlined,
                            color: isCommentOpen ? primaryColor : grey3,
                            size: 20,
                          ),
                          SizedBox(width: 8),
                          Text(
                            '${post['comment_count'] ?? 0}',
                            style: TextStyle(
                              fontFamily: 'Poppins',
                              fontSize: 12,
                              color: isCommentOpen ? primaryColor : grey3,
                            ),
                          ),
                        ],
                      ),
                    ),
                    Spacer(),
                    // Share Button
                    GestureDetector(
                      onTap: () => _showShareOptions(postIndex),
                      child: Icon(
                        isShareOpen ? Icons.share : Icons.share_outlined,
                        color: isShareOpen ? primaryColor : grey3,
                        size: 20,
                      ),
                    ),
                  ],
                ),
                // Comment Box
                if (isCommentOpen) ...[
                  SizedBox(height: 16),
                  Container(
                    padding: EdgeInsets.all(12),
                    decoration: BoxDecoration(
                      color: grey1.withValues(alpha: 0.3),
                      borderRadius: BorderRadius.circular(8),
                    ),
                    child: Row(
                      children: [
                        Expanded(
                          child: TextField(
                            onChanged: (value) =>
                                _updateCommentText(postIndex, value),
                            decoration: InputDecoration(
                              hintText: 'Write a comment...',
                              border: InputBorder.none,
                              hintStyle: TextStyle(
                                fontFamily: 'Poppins',
                                fontSize: 12,
                                color: grey3,
                              ),
                            ),
                            style: TextStyle(
                              fontFamily: 'Poppins',
                              fontSize: 12,
                              color: titlecolor,
                            ),
                          ),
                        ),
                        SizedBox(width: 8),
                        GestureDetector(
                          onTap: () => _submitComment(postIndex),
                          child: Icon(
                            Icons.send,
                            color: primaryColor,
                            size: 20,
                          ),
                        ),
                      ],
                    ),
                  ),
                ],
                // Display existing comments
                if ((post['comments'] ?? []).isNotEmpty) ...[
                  SizedBox(height: 16),
                  Container(
                    padding: EdgeInsets.all(12),
                    decoration: BoxDecoration(
                      color: grey1.withValues(alpha: 0.1),
                      borderRadius: BorderRadius.circular(8),
                    ),
                    child: Column(
                      crossAxisAlignment: CrossAxisAlignment.start,
                      children: [
                        Text(
                          'Comments',
                          style: TextStyle(
                            fontFamily: 'Poppins',
                            fontSize: 12,
                            fontWeight: FontWeight.w600,
                            color: titlecolor,
                          ),
                        ),
                        SizedBox(height: 8),
                        ...(post['comments'] as List<dynamic>)
                            .map((comment) => Container(
                                  margin: EdgeInsets.only(bottom: 8),
                                  padding: EdgeInsets.all(8),
                                  decoration: BoxDecoration(
                                    color: whiteColor,
                                    borderRadius: BorderRadius.circular(6),
                                    border: Border.all(
                                        color: grey1.withValues(alpha: 0.2)),
                                  ),
                                  child: Column(
                                    crossAxisAlignment:
                                        CrossAxisAlignment.start,
                                    children: [
                                      Row(
                                        children: [
                                          Container(
                                            width: 24,
                                            height: 24,
                                            decoration: BoxDecoration(
                                              color: primaryColor.withValues(
                                                  alpha: 0.1),
                                              borderRadius:
                                                  BorderRadius.circular(12),
                                            ),
                                            child: Center(
                                              child: Icon(
                                                Icons.person,
                                                color: primaryColor,
                                                size: 12,
                                              ),
                                            ),
                                          ),
                                          SizedBox(width: 8),
                                          Expanded(
                                            child: Text(
                                              comment['user']?['full_name'] ??
                                                  comment['user']
                                                      ?['username'] ??
                                                  'Unknown User',
                                              style: TextStyle(
                                                fontFamily: 'Poppins',
                                                fontSize: 11,
                                                fontWeight: FontWeight.w600,
                                                color: titlecolor,
                                              ),
                                            ),
                                          ),
                                          Text(
                                            _formatCommentTimestamp(
                                                comment['created_at']),
                                            style: TextStyle(
                                              fontFamily: 'Poppins',
                                              fontSize: 10,
                                              color: grey3,
                                            ),
                                          ),
                                        ],
                                      ),
                                      SizedBox(height: 4),
                                      Text(
                                        comment['content'] ?? '',
                                        style: TextStyle(
                                          fontFamily: 'Poppins',
                                          fontSize: 12,
                                          color: titlecolor,
                                        ),
                                      ),
                                    ],
                                  ),
                                ))
                            .toList(),
                      ],
                    ),
                  ),
                ],
                // Share Options
                if (isShareOpen) ...[
                  SizedBox(height: 16),
                  Container(
                    padding: EdgeInsets.all(16),
                    decoration: BoxDecoration(
                      color: grey1.withValues(alpha: 0.1),
                      borderRadius: BorderRadius.circular(8),
                    ),
                    child: Column(
                      crossAxisAlignment: CrossAxisAlignment.start,
                      children: [
                        Text(
                          'Share to:',
                          style: TextStyle(
                            fontFamily: 'Poppins',
                            fontSize: 12,
                            fontWeight: FontWeight.w600,
                            color: titlecolor,
                          ),
                        ),
                        SizedBox(height: 12),
                        Wrap(
                          spacing: 12,
                          runSpacing: 8,
                          children: sharePlatforms.entries.map((entry) {
                            String platform = entry.key;
                            Map<String, dynamic> config = entry.value;
                            return _buildShareOption(
                              platform,
                              config['icon'],
                              config['color'],
                              postIndex,
                            );
                          }).toList(),
                        ),
                      ],
                    ),
                  ),
                ],
              ],
            ),
          ),
        ],
      ),
    );
  }

  /// Build share option button
  Widget _buildShareOption(
      String platform, IconData icon, Color color, int postIndex) {
    return GestureDetector(
      onTap: () => _shareToPlatform(platform, postIndex),
      child: Container(
        padding: EdgeInsets.symmetric(horizontal: 12, vertical: 8),
        decoration: BoxDecoration(
          color: color.withValues(alpha: 0.1),
          borderRadius: BorderRadius.circular(20),
          border: Border.all(color: color.withValues(alpha: 0.3)),
        ),
        child: Row(
          mainAxisSize: MainAxisSize.min,
          children: [
            Icon(icon, color: color, size: 16),
            SizedBox(width: 6),
            Text(
              sharePlatforms[platform]?['text'] ?? platform,
              style: TextStyle(
                fontFamily: 'Poppins',
                fontSize: 10,
                fontWeight: FontWeight.w500,
                color: color,
              ),
            ),
          ],
        ),
      ),
    );
  }

  /// Build loading widget
  Widget _buildLoadingWidget() {
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
            'Loading posts...',
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

  /// Build empty state widget
  Widget _buildEmptyState() {
    return Center(
      child: Column(
        mainAxisAlignment: MainAxisAlignment.center,
        children: [
          Icon(
            Icons.forum_outlined,
            size: 64,
            color: grey3,
          ),
          SizedBox(height: 16),
          Text(
            'NO POSTS',
            style: TextStyle(
              fontFamily: 'Poppins',
              fontSize: 18,
              fontWeight: FontWeight.w600,
              color: titlecolor,
            ),
          ),
          SizedBox(height: 8),
          Text(
            'No posts available for $selectedYear',
            style: TextStyle(
              fontFamily: 'Poppins',
              fontSize: 14,
              color: grey3,
            ),
          ),
        ],
      ),
    );
  }

  /// Show dialog to create new post
  Future<String?> _showCreatePostDialog() async {
    print('🔍 DEBUG: Starting _showCreatePostDialog');
    return await showDialog<String>(
      context: context,
      builder: (BuildContext context) {
        print('🔍 DEBUG: Building dialog');
        String? newPostContent;
        return AlertDialog(
          title: Text('Create New Post'),
          content: TextField(
            autofocus: true,
            decoration: InputDecoration(
              hintText: 'What\'s on your mind?',
              border: OutlineInputBorder(),
            ),
            onChanged: (value) {
              print('🔍 DEBUG: Text field changed: $value');
              newPostContent = value;
            },
          ),
          actions: <Widget>[
            TextButton(
              onPressed: () {
                print('🔍 DEBUG: Cancel button pressed');
                Navigator.of(context).pop();
              },
              child: Text('Cancel'),
            ),
            TextButton(
              onPressed: () {
                print(
                    '🔍 DEBUG: Post button pressed, content: $newPostContent');
                Navigator.of(context).pop(newPostContent);
              },
              child: Text('Post'),
            ),
          ],
        );
      },
    );
  }

  @override
  Widget build(BuildContext context) {
    print('🔍 DEBUG: Building CavityScreen');
    print('🔍 DEBUG: isLoading: $isLoading');
    print('🔍 DEBUG: allPosts.length: ${allPosts.length}');
    print('🔍 DEBUG: allPosts.isEmpty: ${allPosts.isEmpty}');

    return Scaffold(
      backgroundColor: color3,
      body: SafeArea(
        child: Stack(
          children: [
            // Main Content
            Column(
              children: [
                // Header
                _buildHeader(),
                // Feed Content
                Expanded(
                  child: isLoading
                      ? _buildLoadingWidget()
                      : allPosts.isEmpty
                          ? _buildEmptyState()
                          : RefreshIndicator(
                              onRefresh: _loadData,
                              child: ListView.builder(
                                padding: EdgeInsets.symmetric(vertical: 8),
                                itemCount: allPosts.length,
                                itemBuilder: (context, index) {
                                  print(
                                      '🔍 DEBUG: Building post block at index $index');
                                  return _buildPostBlock(
                                      allPosts[index], index);
                                },
                              ),
                            ),
                ),
              ],
            ),
            // Overlay for outside tap detection
            if (isDropdownOpen)
              Positioned.fill(
                child: GestureDetector(
                  onTap: () {
                    setState(() {
                      isDropdownOpen = false;
                    });
                  },
                  child: Container(
                    color: Colors.transparent,
                  ),
                ),
              ),
            // Year Selection Modal
            _buildYearSelectionModal(),
          ],
        ),
      ),
      // Floating Action Button (Optional)
      floatingActionButton: FloatingActionButton(
        onPressed: () async {
          print('🔍 DEBUG: FloatingActionButton pressed');
          // Show dialog to create new post
          String? newPostContent = await _showCreatePostDialog();
          print('🔍 DEBUG: Dialog returned content: $newPostContent');

          if (newPostContent != null && newPostContent.trim().isNotEmpty) {
            print('🔍 DEBUG: ===== STARTING POST CREATION ====');
            print(
                '🔍 DEBUG: Attempting to create post with content: $newPostContent');
            print('🔍 DEBUG: Selected year: $selectedYear');
            print('🔍 DEBUG: Content length: ${newPostContent.length}');
            print('🔍 DEBUG: Content trimmed: ${newPostContent.trim()}');

            bool success = await CavityApiService.createPost(
                newPostContent.trim(),
                year: selectedYear);

            print('🔍 DEBUG: CavityApiService.createPost returned: $success');

            if (success) {
              print(
                  '🔍 DEBUG: Post creation successful, showing success message');
              ScaffoldMessenger.of(context).showSnackBar(
                SnackBar(
                  content: Text('Post created successfully!'),
                  backgroundColor: primaryColor,
                ),
              );
              // Reload data to show new post
              print('🔍 DEBUG: Reloading data to show new post');
              _loadData();
            } else {
              print('🔍 DEBUG: Post creation failed, showing error message');
              ScaffoldMessenger.of(context).showSnackBar(
                SnackBar(
                  content: Text('Failed to create post'),
                  backgroundColor: Colors.red,
                ),
              );
            }
            print('🔍 DEBUG: ===== POST CREATION COMPLETED ====');
          } else {
            print('🔍 DEBUG: No content provided or content is empty');
            print('🔍 DEBUG: newPostContent: $newPostContent');
            print(
                '🔍 DEBUG: newPostContent?.trim().isEmpty: ${newPostContent?.trim().isEmpty}');
          }
        },
        backgroundColor: primaryColor,
        child: Icon(Icons.add, color: whiteColor),
      ),
    );
  }
}
