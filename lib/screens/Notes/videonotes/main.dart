import 'dart:convert';
import 'package:flutter/material.dart';
import 'package:frontend/screens/notification/notification.dart';
import 'package:frontend/utils/avatar.dart';
import 'package:frontend/utils/responsive.dart';
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
  Measurements? size;
  late Future<List<Map<String, dynamic>>> videoListFuture;
  int _selectedIndex = 3; // Notes tab is active

  @override
  void initState() {
    super.initState();
    videoListFuture = fetchTopics();
  }

  /// Fetches all video topics from the API
  Future<List<Map<String, dynamic>>> fetchTopics() async {
    try {
      final response = await http.get(
        Uri.parse('${BaseUrl.baseUrl}/notes/videos/topics/'),
        headers: {
          'Content-Type': 'application/json',
          'Accept': 'application/json',
        },
      );

      print('Video API Response Status: ${response.statusCode}');
      print('Video API Response Body: ${response.body}');

      if (response.statusCode == 200) {
        final List<dynamic> data = json.decode(response.body);
        return List<Map<String, dynamic>>.from(data);
      } else {
        throw Exception('Failed to load video topics: ${response.statusCode}');
      }
    } catch (e) {
      print('Error fetching video topics: $e');
      return [];
    }
  }

  /// Navigate to video sub screen
  void _navigateToVideoSubScreen(Map<String, dynamic> videoTopic) {
    // You'll need to update this to navigate to the correct screen
    // based on the topic. The original code was commented out.
    // This is a placeholder.
    print('Navigating to video topic: ${videoTopic['topic']}');
  }

  /// Builds individual video topic cards
  Widget _buildVideoCard(Map<String, dynamic> videoTopic) {
    String topicTitle = videoTopic['topic'] ?? 'Unknown Topic';
    int videoCount = videoTopic['videos'] ?? 0;
    String countText = '$videoCount video${videoCount != 1 ? 's' : ''}';

    return GestureDetector(
      onTap: () => _navigateToVideoSubScreen(videoTopic),
      child: Container(
        margin: EdgeInsets.symmetric(horizontal: 16, vertical: 6),
        padding: EdgeInsets.all(12),
        decoration: BoxDecoration(
          color: whiteColor,
          borderRadius: BorderRadius.circular(10),
          boxShadow: [
            BoxShadow(
              color: grey3.withOpacity(0.2),
              blurRadius: 4,
              offset: Offset(0, 2),
            ),
          ],
        ),
        child: Stack(
          children: [
            // Topic title at the top left
            Align(
              alignment: Alignment.topLeft,
              child: Padding(
                padding: const EdgeInsets.only(top: 8.0, left: 8.0),
                child: Text(
                  topicTitle,
                  style: TextStyle(
                    fontFamily: 'Poppins',
                    fontSize: 16,
                    fontWeight: FontWeight.w600,
                    color: titlecolor,
                  ),
                ),
              ),
            ),
            // Video count at the bottom right
            Align(
              alignment: Alignment.bottomRight,
              child: Padding(
                padding: const EdgeInsets.only(bottom: 8.0, right: 8.0),
                child: Text(
                  countText,
                  style: TextStyle(
                    fontFamily: 'Poppins',
                    fontSize: 14,
                    color: grey3,
                  ),
                ),
              ),
            ),
          ],
        ),
      ),
    );
  }

  @override
  Widget build(BuildContext context) {
    size = Measurements(MediaQuery.of(context).size);
    return Scaffold(
      backgroundColor: color3,
      appBar: AppBar(
        leading: IconButton(
          icon: Icon(
            Icons.arrow_back_ios_new,
            color: primaryColor,
            size: size!.hp(3.5),
            weight: 700,
          ),
          onPressed: () {
            Navigator.of(context).pop();
          },
        ),
        backgroundColor: Colors.white,
        elevation: 0.2,
        automaticallyImplyLeading: false,
        centerTitle: true,
        title: SizedBox(
          height: 250,
          width: 200,
          child: Image.asset(edvoyagelogo1),
        ),
        actions: [
          IconButton(
              icon: Icon(
                Icons.notifications,
                color: primaryColor,
              ),
              onPressed: () {
                Navigator.push(
                    context,
                    MaterialPageRoute(
                        builder: (context) => NotificationScreen()));
              })
        ],
      ),
      body: SafeArea(
        child: Column(
          children: [
            Expanded(
              child: FutureBuilder<List<Map<String, dynamic>>>(
                future: videoListFuture,
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
                            'Loading Topics...',
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
                          Icon(Icons.error_outline, size: 48, color: grey3),
                          SizedBox(height: 16),
                          Text(
                            'Failed to load topics',
                            style: TextStyle(
                              fontFamily: 'Poppins',
                              fontSize: 16,
                              color: grey3,
                            ),
                          ),
                          SizedBox(height: 8),
                          ElevatedButton(
                            onPressed: () {
                              setState(() {
                                videoListFuture = fetchTopics();
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

                  final videoTopics = snapshot.data ?? [];

                  if (videoTopics.isEmpty) {
                    return Center(
                      child: Text(
                        'No video topics available',
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
                    itemCount: videoTopics.length,
                    itemBuilder: (context, index) {
                      return _buildVideoCard(videoTopics[index]);
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
