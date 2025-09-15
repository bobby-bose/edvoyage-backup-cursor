import 'dart:convert';
import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;
import 'package:notes/screens/constants.dart';
import 'package:notes/screens/logo.dart';
import 'package:notes/screens/topbar.dart';

// --- DATA MODEL for Video ---
class Video {
  final int id;
  final String title;
  final String videoUrl;
  final String logo;
  final int duration;
  final bool isFree;
  final String subjectName;
  final String doctorName;

  Video({
    required this.id,
    required this.title,
    required this.videoUrl,
    required this.logo,
    required this.duration,
    required this.isFree,
    required this.subjectName,
    required this.doctorName,
  });

  factory Video.fromJson(Map<String, dynamic> json) {
    return Video(
      id: json['id'],
      title: json['title'],
      videoUrl: json['video_url'],
      logo: json['logo'],
      duration: json['duration_in_minutes'],
      isFree: json['is_free'],
      subjectName: json['subject_name'],
      doctorName: json['doctor']['name'],
    );
  }
}

// --- SCREEN THAT ACCEPTS SUBJECT NAME ---
class VideosBySubjectScreen extends StatefulWidget {
  final String subjectName; // Pass this from previous screen

  const VideosBySubjectScreen({super.key, required this.subjectName});

  @override
  State<VideosBySubjectScreen> createState() => _VideosBySubjectScreenState();
}

class _VideosBySubjectScreenState extends State<VideosBySubjectScreen> {
  bool _isLoading = true;
  List<Video> _videos = [];

  @override
  void initState() {
    super.initState();
    _fetchVideosBySubject();
  }

  Future<void> _fetchVideosBySubject() async {
    try {
      final response = await http.get(Uri.parse("${API}videos/"));

      if (response.statusCode == 200) {
        final List<dynamic> data = jsonDecode(response.body);
        print(data);
        // Flter videos by the passed subjectName
        final filteredVideos = data
            .map((json) => Video.fromJson(json))
            .where((video) => video.subjectName == widget.subjectName)
            .toList();

        setState(() {
          _videos = filteredVideos;
          _isLoading = false;
        });
      } else {
        throw Exception('Failed to fetch videos');
      }
    } catch (e) {
      debugPrint("Error fetching videos: $e");
      setState(() {
        _isLoading = false;
      });
    }
  }

  Widget _buildVideoCard(Video video) {
    const Color primaryColor = Color(0xFF008080);

    return InkWell(
      onTap: () {
        print(video.videoUrl);
      },
      borderRadius: BorderRadius.circular(12),
      child: Card(
        margin: const EdgeInsets.symmetric(horizontal: 12, vertical: 6),
        elevation: 2,
        shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(12)),
        child: Padding(
          padding: const EdgeInsets.symmetric(horizontal: 20, vertical: 5),
          child: Row(
            crossAxisAlignment: CrossAxisAlignment.center,
            children: [
              // Thumbnail
              ClipRRect(
                borderRadius: BorderRadius.circular(8),
                child: Image.network(
                  video.logo,
                  width: 120,
                  height: 120,
                  fit: BoxFit.cover,
                  errorBuilder: (context, error, stackTrace) {
                    return Container(
                      width: 120,
                      height: 120,
                      color: Colors.grey[200],
                      child: const Icon(Icons.broken_image, color: Colors.grey),
                    );
                  },
                ),
              ),
              const SizedBox(width: 20),

              // Middle Section: Title, Doctor, Duration
              Expanded(
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.stretch,
                  mainAxisAlignment: MainAxisAlignment.spaceBetween,

                  children: [
                    Text(
                      video.title,
                      style: const TextStyle(
                        fontSize: 30,
                        fontWeight: FontWeight.bold,
                        color: primaryColor,
                      ),
                    ),
                    const SizedBox(height: 10),
                    Text(
                      video.doctorName,
                      style: const TextStyle(fontSize: 20, color: Colors.black),
                      maxLines: 1,
                      overflow: TextOverflow.ellipsis,
                    ),
                    const SizedBox(height: 10),
                    Row(
                      children: [
                        const Icon(
                          Icons.access_time,
                          size: 20,
                          color: Colors.black,
                        ),
                        const SizedBox(width: 4),
                        Text(
                          "${video.duration} Min",
                          style: const TextStyle(
                            fontSize: 20,
                            fontWeight: FontWeight.bold,
                            color: Colors.black,
                          ),
                        ),
                      ],
                    ),
                  ],
                ),
              ),

              // Right Badge (Free / Premium)
              Column(
                mainAxisAlignment: MainAxisAlignment.center,
                children: [
                  Icon(
                    video.isFree ? Icons.lock_open : Icons.lock,
                    color: video.isFree ? primaryColor : Colors.orange,
                  ),
                  Text(
                    video.isFree ? "FREE" : "PREMIUM",
                    style: TextStyle(
                      fontSize: 12,
                      fontWeight: FontWeight.bold,
                      color: video.isFree ? primaryColor : Colors.orange,
                    ),
                  ),
                ],
              ),
            ],
          ),
        ),
      ),
    );
  }

  @override
  Widget build(BuildContext context) {
    const Color primaryColor = Color(0xFF008080);

    return Scaffold(
      appBar: CustomLogoAppBar(),
      body: Column(
        children: [
          // ADDED: The Topbar widget at the top
          Topbar(firstText: 'Medical Videos', secondText: widget.subjectName),
          // The rest of your body logic, now wrapped in an Expanded widget
          Expanded(
            child: _isLoading
                ? const Center(child: CircularProgressIndicator())
                : _videos.isEmpty
                ? Center(
                    child: Text(
                      'No videos available for ${widget.subjectName}',
                      style: const TextStyle(fontSize: 16),
                    ),
                  )
                : ListView.builder(
                    itemCount: _videos.length,
                    itemBuilder: (context, index) {
                      return _buildVideoCard(_videos[index]);
                    },
                  ),
          ),
        ],
      ),
    );
  }
}
