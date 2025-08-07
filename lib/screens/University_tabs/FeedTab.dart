import 'dart:convert';
import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;
import 'package:frontend/utils/colors/colors.dart';
import 'package:frontend/utils/responsive.dart';
import 'package:frontend/_env/env.dart';

class FeedTab extends StatefulWidget {
  final int universityId;

  const FeedTab({super.key, required this.universityId});

  @override
  State<FeedTab> createState() => _FeedTabState();
}

class _FeedTabState extends State<FeedTab> {
  late Future<List<dynamic>> feedsFuture;

  @override
  void initState() {
    super.initState();
    feedsFuture = fetchFeeds();
  }

  Future<List<dynamic>> fetchFeeds() async {
    try {
      print(
          '🔍 DEBUG: Fetching feeds for university ID: ${widget.universityId}');

      // Use the university detail endpoint to get feed data
      final response = await http.get(
        Uri.parse('${BaseUrl.universityList}${widget.universityId}/'),
      );

      print('🔍 DEBUG: Feed API Response Status: ${response.statusCode}');

      if (response.statusCode == 200) {
        final data = json.decode(response.body);
        print('🔍 DEBUG: Feed API Response Data: ${data.toString()}');

        // The feed data is nested in the university response
        if (data is Map && data.containsKey('data')) {
          final universityData = data['data'];
          if (universityData is Map && universityData.containsKey('feed')) {
            print(
                '🔍 DEBUG: Found feed data: ${universityData['feed'].length} feeds');
            return universityData['feed'];
          }
        }

        // Fallback: check if feed is directly in the response
        if (data is Map && data.containsKey('feed')) {
          print(
              '🔍 DEBUG: Found feed data directly: ${data['feed'].length} feeds');
          return data['feed'];
        }

        print('🔍 DEBUG: No feed data found in response');
        return [];
      } else {
        print(
            '🔍 DEBUG: API request failed with status: ${response.statusCode}');
        throw Exception('Failed to load feeds: HTTP ${response.statusCode}');
      }
    } catch (e) {
      print('🔍 DEBUG: Error fetching feeds: $e');
      throw Exception('Failed to load feeds: $e');
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: color3,
      body: FutureBuilder<List<dynamic>>(
        future: feedsFuture,
        builder: (context, snapshot) {
          if (snapshot.connectionState == ConnectionState.waiting) {
            return Center(
              child: CircularProgressIndicator(
                color: Cprimary,
              ),
            );
          } else if (snapshot.hasError) {
            return Center(
              child: Column(
                mainAxisAlignment: MainAxisAlignment.center,
                children: [
                  Icon(
                    Icons.error_outline,
                    color: Colors.red,
                    size: 48,
                  ),
                  SizedBox(height: 16),
                  Text(
                    'Error loading feeds',
                    style: TextStyle(
                      fontSize: 16,
                      fontWeight: FontWeight.bold,
                      color: Colors.red,
                    ),
                  ),
                  SizedBox(height: 8),
                  Text(
                    '${snapshot.error}',
                    style: TextStyle(
                      fontSize: 12,
                      color: Colors.grey,
                    ),
                    textAlign: TextAlign.center,
                  ),
                ],
              ),
            );
          } else if (!snapshot.hasData || snapshot.data!.isEmpty) {
            return Center(
              child: Column(
                mainAxisAlignment: MainAxisAlignment.center,
                children: [
                  Icon(
                    Icons.feed_outlined,
                    color: Colors.grey,
                    size: 48,
                  ),
                  SizedBox(height: 16),
                  Text(
                    'No feeds available',
                    style: TextStyle(
                      fontSize: 16,
                      fontWeight: FontWeight.bold,
                      color: Colors.grey,
                    ),
                  ),
                  SizedBox(height: 8),
                  Text(
                    'This university has not posted any feeds yet.',
                    style: TextStyle(
                      fontSize: 12,
                      color: Colors.grey,
                    ),
                    textAlign: TextAlign.center,
                  ),
                ],
              ),
            );
          }

          final feeds = snapshot.data!;
          print('🔍 DEBUG: Building feeds list with ${feeds.length} feeds');

          return ListView.builder(
            itemCount: feeds.length,
            itemBuilder: (context, index) {
              final feed = feeds[index];
              print(
                  '🔍 DEBUG: Building feed $index: ${feed['title'] ?? 'Unknown'}');

              return Card(
                shape: RoundedRectangleBorder(
                  borderRadius: BorderRadius.circular(15),
                ),
                elevation: 5,
                margin: EdgeInsets.all(10),
                child: Padding(
                  padding: const EdgeInsets.all(18.0),
                  child: Column(
                    crossAxisAlignment: CrossAxisAlignment.start,
                    children: [
                      Row(
                        children: [
                          // User Avatar
                          Container(
                            width: 50,
                            height: 50,
                            decoration: BoxDecoration(
                              color: thirdColor,
                              shape: BoxShape.circle,
                            ),
                            child: feed['avatar_url'] != null
                                ? ClipOval(
                                    child: Image.network(
                                      feed['avatar_url'],
                                      fit: BoxFit.cover,
                                      errorBuilder:
                                          (context, error, stackTrace) {
                                        return Icon(
                                          Icons.person,
                                          color: Colors.white,
                                          size: 24,
                                        );
                                      },
                                    ),
                                  )
                                : Icon(
                                    Icons.person,
                                    color: Colors.white,
                                    size: 24,
                                  ),
                          ),
                          hGap(10),
                          Column(
                            mainAxisAlignment: MainAxisAlignment.center,
                            crossAxisAlignment: CrossAxisAlignment.start,
                            children: [
                              Text(
                                feed['user_name'] ?? 'Unknown User',
                                style: TextStyle(
                                  fontFamily: 'Poppins',
                                  fontSize: 17,
                                  color: Cprimary,
                                  fontWeight: FontWeight.w500,
                                ),
                              ),
                              Text(
                                feed['date_posted'] != null
                                    ? feed['date_posted']
                                        .toString()
                                        .substring(0, 10)
                                    : 'Unknown Date',
                                style: TextStyle(
                                  fontSize: 17,
                                  fontFamily: 'Poppins',
                                  color: Cprimary,
                                  fontWeight: FontWeight.w400,
                                ),
                              ),
                            ],
                          ),
                        ],
                      ),
                      Divider(
                        thickness: 1,
                        color: ttext2,
                      ),
                      Column(
                        crossAxisAlignment: CrossAxisAlignment.start,
                        children: [
                          vGap(5),
                          Text(
                            feed['title'] ?? 'No Title',
                            style: TextStyle(
                              fontSize: 17,
                              fontFamily: 'Poppins',
                              color: titlecolor,
                              fontWeight: FontWeight.w700,
                            ),
                          ),
                          vGap(5),
                          Text(
                            feed['description'] ?? 'No description available',
                            textAlign: TextAlign.justify,
                            style: TextStyle(
                              fontFamily: 'Poppins',
                              fontSize: 14,
                              fontWeight: FontWeight.w400,
                            ),
                          ),
                          vGap(5),
                        ],
                      ),
                    ],
                  ),
                ),
              );
            },
          );
        },
      ),
    );
  }
}
