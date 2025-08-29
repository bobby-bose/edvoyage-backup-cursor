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
    videoListFuture = fetchVideos();
  }

  /// Fetches all videos from the API
  Future<List<Map<String, dynamic>>> fetchVideos() async {
    try {
      final response = await http.get(
        Uri.parse('${BaseUrl.baseUrl}/notes/notesvideos/'),
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
        throw Exception('Failed to load videos: ${response.statusCode}');
      }
    } catch (e) {
      print('Error fetching videos: $e');
      // Return empty list if API fails
      return [];
    }
  }

  /// Navigate to video sub screen
  void _navigateToVideoSubScreen(Map<String, dynamic> video) {
    // Navigator.push(
    //   context,
    //   MaterialPageRoute(
    //     builder: (context) => VideoNotesSubScreen(
    //       categoryTitle: video['title'] ?? 'Unknown Video',
    //       categoryId: video['id'] ?? 0, // Or pass videoId if needed
    //       videoUrl: video[
    //         'videoId'], // Make sure VideoNotesSubScreen accepts videoUrl
    //   ),
    // ),
    // );
    print('Navigating to video: ${video['title']}');
  }

  /// Builds individual video cards
  Widget _buildVideoCard(Map<String, dynamic> video) {
    return GestureDetector(
      onTap: () => _navigateToVideoSubScreen(video),
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
        child: Row(
          children: [
            // Thumbnail
            // ClipRRect(
            //   borderRadius: BorderRadius.circular(8),
            //   child: Image.network(
            //     video['thumbnailUrl'] ?? '',
            //     width: 100,
            //     height: 60,
            //     fit: BoxFit.cover,
            //   ),
            // ),
            SizedBox(width: 12),
            // Video info
            Expanded(
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  Text(
                    video['title'] ?? 'Unknown Video',
                    style: TextStyle(
                      fontFamily: 'Poppins',
                      fontSize: 16,
                      fontWeight: FontWeight.w600,
                      color: titlecolor,
                    ),
                  ),
                  SizedBox(height: 4),
                  Text(
                    video['doctor'] ?? '',
                    style: TextStyle(
                      fontFamily: 'Poppins',
                      fontSize: 14,
                      color: grey3,
                    ),
                  ),
                  SizedBox(height: 2),
                  Text(
                    video['duration'] ?? '0 Min',
                    style: TextStyle(
                      fontFamily: 'Poppins',
                      fontSize: 12,
                      color: grey3,
                    ),
                  ),
                ],
              ),
            ),
            Icon(Icons.arrow_forward_ios, color: grey3, size: 16),
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
            size: size!.hp(3.5), // Slightly larger than default
            weight: 700, // For a little thickness (Flutter 3.7+)
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
          height: 250, // Set the width of the container
          width: 200, // Set the height of the container
          child:
              Image.asset(edvoyagelogo1), // Replace with the actual image path
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
                          Icon(Icons.error_outline, size: 48, color: grey3),
                          SizedBox(height: 16),
                          Text(
                            'Failed to load videos',
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
                                videoListFuture = fetchVideos();
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

                  final videos = snapshot.data ?? [];

                  if (videos.isEmpty) {
                    return Center(
                      child: Text(
                        'No videos available',
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
                    itemCount: videos.length,
                    itemBuilder: (context, index) {
                      return _buildVideoCard(videos[index]);
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
