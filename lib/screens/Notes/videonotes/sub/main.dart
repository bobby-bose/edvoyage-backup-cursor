import 'dart:convert';
import 'package:flutter/material.dart';
import 'package:flutter/services.dart';
import 'package:frontend/utils/colors/colors.dart';
import 'package:frontend/screens/Notes/videonotes/sub/cards.dart';
import 'package:frontend/screens/Notes/videonotes/video_player/main.dart';
import 'package:frontend/widgets/botttom_nav.dart';
import 'package:frontend/Services/notes_api_service.dart';

// Error types for better error handling
enum ApiErrorType { networkError, serverError, notFound, unauthorized, unknown }

class ApiError {
  final ApiErrorType type;
  final String message;
  final int? statusCode;

  ApiError(this.type, this.message, {this.statusCode});
}

class VideoNotesSubScreen extends StatefulWidget {
  final String categoryTitle;
  final int categoryId; // This is actually topicId now

  const VideoNotesSubScreen({
    super.key,
    required this.categoryTitle,
    required this.categoryId,
  });

  @override
  _VideoNotesSubScreenState createState() => _VideoNotesSubScreenState();
}

class _VideoNotesSubScreenState extends State<VideoNotesSubScreen> {
  late Future<List<Map<String, dynamic>>> videoLecturesFuture;
  int _selectedIndex = 3; // Notes tab is active
  bool _isApiConnected = false;
  ApiError? _lastError;

  @override
  void initState() {
    super.initState();
    _testApiConnection();
    videoLecturesFuture = fetchVideoLecturesWithRetry();
  }

  /// Test API connectivity
  Future<void> _testApiConnection() async {
    final isConnected = await NotesApiService.testApiConnection();
    setState(() {
      _isApiConnected = isConnected;
    });
    print(
        '🔍 API Connection Test: ${isConnected ? "✅ Connected" : "❌ Failed"}');
  }

  /// Fetch video lectures with retry logic
  Future<List<Map<String, dynamic>>> fetchVideoLecturesWithRetry({
    int maxRetries = 3,
    int delaySeconds = 1,
  }) async {
    for (int attempt = 1; attempt <= maxRetries; attempt++) {
      try {
        print('🔄 Attempt $attempt of $maxRetries');
        final lectures = await NotesApiService.fetchVideoLectures(
          topicId: widget.categoryId, // This is actually topicId
        );

        // Clear any previous errors
        setState(() {
          _lastError = null;
        });

        return lectures;
      } catch (e) {
        print('❌ Attempt $attempt failed: $e');

        if (attempt == maxRetries) {
          // Set error for UI display
          setState(() {
            _lastError = _parseError(e);
          });
          rethrow;
        }

        // Wait before retry with exponential backoff
        await Future.delayed(Duration(seconds: delaySeconds * attempt));
      }
    }
    throw Exception('Max retries exceeded');
  }

  /// Parse error and return appropriate ApiError
  ApiError _parseError(dynamic error) {
    final errorString = error.toString().toLowerCase();

    if (errorString.contains('network') || errorString.contains('connection')) {
      return ApiError(ApiErrorType.networkError, 'Network connection error');
    } else if (errorString.contains('404') ||
        errorString.contains('not found')) {
      return ApiError(ApiErrorType.notFound, 'Topic not found',
          statusCode: 404);
    } else if (errorString.contains('401') ||
        errorString.contains('unauthorized')) {
      return ApiError(ApiErrorType.unauthorized, 'Unauthorized access',
          statusCode: 401);
    } else if (errorString.contains('500') || errorString.contains('server')) {
      return ApiError(ApiErrorType.serverError, 'Server error',
          statusCode: 500);
    } else {
      return ApiError(ApiErrorType.unknown, 'Unknown error occurred');
    }
  }

  /// Fetches video lectures data from REST API
  Future<List<Map<String, dynamic>>> fetchVideoLectures() async {
    try {
      print(
          '🔍 DEBUG: Fetching video lectures for topic ID: ${widget.categoryId}');

      // Fetch data from REST API
      final lectures = await NotesApiService.fetchVideoLectures(
        topicId: widget.categoryId, // This is actually topicId
      );

      print('✅ Successfully loaded ${lectures.length} video lectures from API');
      return lectures;
    } catch (e) {
      print('❌ Error loading video lectures from API: $e');

      // Return fallback data if API fails
      return _getFallbackData();
    }
  }

  /// Get fallback static data
  List<Map<String, dynamic>> _getFallbackData() {
    return [
      {
        'id': 1,
        'title': 'Gametogenesis',
        'doctor': 'Dr. Sarah Johnson, MD',
        'duration': '30 Min',
        'thumbnailUrl':
            'https://www.topuniversities.com/sites/default/files/harvard_1.jpg',
        'accessType': 'free',
        'videoId': 'video_001'
      },
      {
        'id': 2,
        'title': 'Human Anatomy Overview',
        'doctor': 'Dr. Michael Chen, PhD',
        'duration': '45 Min',
        'thumbnailUrl':
            'https://www.topuniversities.com/sites/default/files/harvard_1.jpg',
        'accessType': 'premium',
        'videoId': 'video_002'
      },
      {
        'id': 3,
        'title': 'Cardiovascular System',
        'doctor': 'Dr. Emily Rodriguez, MD',
        'duration': '35 Min',
        'thumbnailUrl':
            'https://www.topuniversities.com/sites/default/files/harvard_1.jpg',
        'accessType': 'free',
        'videoId': 'video_003'
      },
      {
        'id': 4,
        'title': 'Nervous System Anatomy',
        'doctor': 'Dr. David Kim, PhD',
        'duration': '40 Min',
        'thumbnailUrl':
            'https://www.topuniversities.com/sites/default/files/harvard_1.jpg',
        'accessType': 'premium',
        'videoId': 'video_004'
      },
      {
        'id': 5,
        'title': 'Respiratory System',
        'doctor': 'Dr. Lisa Thompson, MD',
        'duration': '25 Min',
        'thumbnailUrl':
            'https://www.topuniversities.com/sites/default/files/harvard_1.jpg',
        'accessType': 'free',
        'videoId': 'video_005'
      },
    ];
  }

  /// Navigate to video player screen with enhanced analytics
  void _navigateToVideoPlayer(Map<String, dynamic> videoData) async {
    // Track video view for analytics
    try {
      await NotesApiService.trackVideoView(videoData['id']);

      // Track additional analytics
      await _trackVideoAnalytics(videoData);
    } catch (e) {
      print('⚠️ Failed to track video view: $e');
    }

    // Add category title to video data
    Map<String, dynamic> enhancedVideoData = Map.from(videoData);
    enhancedVideoData['categoryTitle'] = widget.categoryTitle;
    enhancedVideoData['videoUrl'] =
        'https://www.youtube.com/watch?v=dQw4w9WgXcQ'; // Example YouTube URL

    Navigator.push(
      context,
      MaterialPageRoute(
        builder: (context) => VideoPlayerScreen(videoData: enhancedVideoData),
      ),
    );
  }

  /// Track additional video analytics
  Future<void> _trackVideoAnalytics(Map<String, dynamic> videoData) async {
    final analytics = {
      'video_id': videoData['id'],
      'topic_id': widget.categoryId, // This is actually topicId
      'topic_title': widget.categoryTitle,
      'access_type': videoData['accessType'],
      'timestamp': DateTime.now().toIso8601String(),
    };

    print('📊 Analytics: $analytics');
  }

  /// Refresh video lectures data
  void _refreshVideoLectures() {
    setState(() {
      _lastError = null;
      videoLecturesFuture = fetchVideoLecturesWithRetry();
    });
  }

  /// Build error widget based on error type
  Widget _buildErrorWidget(ApiError error) {
    String title, message;
    IconData icon;

    switch (error.type) {
      case ApiErrorType.networkError:
        title = 'Network Error';
        message = 'Please check your internet connection and try again';
        icon = Icons.wifi_off;
        break;
      case ApiErrorType.notFound:
        title = 'Topic Not Found';
        message = 'The requested topic does not exist or has been removed';
        icon = Icons.search_off;
        break;
      case ApiErrorType.serverError:
        title = 'Server Error';
        message = 'Our servers are experiencing issues. Please try again later';
        icon = Icons.error_outline;
        break;
      case ApiErrorType.unauthorized:
        title = 'Access Denied';
        message = 'You are not authorized to access this content';
        icon = Icons.lock;
        break;
      case ApiErrorType.unknown:
        title = 'Something Went Wrong';
        message = 'An unexpected error occurred. Please try again';
        icon = Icons.help_outline;
        break;
    }

    return Center(
      child: Column(
        mainAxisAlignment: MainAxisAlignment.center,
        children: [
          Icon(
            icon,
            size: 48,
            color: grey3,
          ),
          SizedBox(height: 16),
          Text(
            title,
            style: TextStyle(
              fontFamily: 'Poppins',
              fontSize: 18,
              fontWeight: FontWeight.w600,
              color: grey3,
            ),
          ),
          SizedBox(height: 8),
          Padding(
            padding: EdgeInsets.symmetric(horizontal: 32),
            child: Text(
              message,
              textAlign: TextAlign.center,
              style: TextStyle(
                fontFamily: 'Poppins',
                fontSize: 14,
                color: grey3,
              ),
            ),
          ),
          SizedBox(height: 24),
          Row(
            mainAxisAlignment: MainAxisAlignment.center,
            children: [
              ElevatedButton(
                onPressed: _refreshVideoLectures,
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
              SizedBox(width: 12),
              if (!_isApiConnected)
                ElevatedButton(
                  onPressed: () {
                    _testApiConnection();
                    _refreshVideoLectures();
                  },
                  style: ElevatedButton.styleFrom(
                    backgroundColor: secondaryColor,
                    shape: RoundedRectangleBorder(
                      borderRadius: BorderRadius.circular(8),
                    ),
                  ),
                  child: Text(
                    'Check Connection',
                    style: TextStyle(
                      fontFamily: 'Poppins',
                      color: whiteColor,
                      fontSize: 14,
                    ),
                  ),
                ),
            ],
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
        title: Text(widget.categoryTitle),
        backgroundColor: primaryColor,
        elevation: 0,
        leading: IconButton(
          icon: Icon(Icons.arrow_back_ios, color: whiteColor),
          onPressed: () {
            Navigator.pop(context);
          },
        ),
        actions: [
          // API connection status indicator
          if (!_isApiConnected)
            IconButton(
              icon: Icon(Icons.wifi_off, color: Colors.orange),
              onPressed: () {
                _testApiConnection();
                _refreshVideoLectures();
              },
              tooltip: 'API Connection Issue - Tap to retry',
            ),
          IconButton(
            icon: Icon(Icons.refresh, color: whiteColor),
            onPressed: _refreshVideoLectures,
            tooltip: 'Refresh lectures',
          ),
        ],
      ),
      body: SafeArea(
        child: Column(
          children: [
            Expanded(
              child: FutureBuilder<List<Map<String, dynamic>>>(
                future: videoLecturesFuture,
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
                            'Loading Lectures...',
                            style: TextStyle(
                              fontFamily: 'Poppins',
                              fontSize: 16,
                              color: grey3,
                            ),
                          ),
                          if (!_isApiConnected) ...[
                            SizedBox(height: 8),
                            Text(
                              'Using cached data',
                              style: TextStyle(
                                fontFamily: 'Poppins',
                                fontSize: 12,
                                color: Colors.orange,
                              ),
                            ),
                          ],
                        ],
                      ),
                    );
                  }

                  if (snapshot.hasError || _lastError != null) {
                    return _buildErrorWidget(_lastError ??
                        ApiError(ApiErrorType.unknown,
                            snapshot.error?.toString() ?? 'Unknown error'));
                  }

                  final lectures = snapshot.data ?? [];

                  if (lectures.isEmpty) {
                    return Center(
                      child: Column(
                        mainAxisAlignment: MainAxisAlignment.center,
                        children: [
                          Icon(
                            Icons.video_library_outlined,
                            size: 48,
                            color: grey3,
                          ),
                          SizedBox(height: 16),
                          Text(
                            'No lectures available',
                            style: TextStyle(
                              fontFamily: 'Poppins',
                              fontSize: 16,
                              color: grey3,
                            ),
                          ),
                          SizedBox(height: 8),
                          Text(
                            'Check back later for new content',
                            style: TextStyle(
                              fontFamily: 'Poppins',
                              fontSize: 14,
                              color: grey3,
                            ),
                          ),
                          SizedBox(height: 16),
                          ElevatedButton(
                            onPressed: _refreshVideoLectures,
                            style: ElevatedButton.styleFrom(
                              backgroundColor: primaryColor,
                              shape: RoundedRectangleBorder(
                                borderRadius: BorderRadius.circular(8),
                              ),
                            ),
                            child: Text(
                              'Refresh',
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

                  return RefreshIndicator(
                    onRefresh: () async {
                      _refreshVideoLectures();
                    },
                    color: primaryColor,
                    child: ListView.builder(
                      padding: EdgeInsets.symmetric(vertical: 10),
                      physics: BouncingScrollPhysics(),
                      itemCount: lectures.length,
                      itemBuilder: (context, index) {
                        final lecture = lectures[index];
                        return VideoLectureCard(
                          lecture: lecture,
                          onTap: () => _navigateToVideoPlayer(lecture),
                        );
                      },
                    ),
                  );
                },
              ),
            ),
            BottomButton(
              selectedIndex: _selectedIndex,
              onTap: () {
                // Handle any additional tap logic if needed
              },
            ),
          ],
        ),
      ),
    );
  }
}
