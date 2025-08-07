import 'dart:convert';
import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;
import 'package:frontend/utils/colors/colors.dart';
import 'package:frontend/_env/env.dart';

class GalleryTab extends StatefulWidget {
  final int universityId;
  const GalleryTab({super.key, required this.universityId});

  @override
  _GalleryTabState createState() => _GalleryTabState();
}

class _GalleryTabState extends State<GalleryTab> {
  late Future<List<String>> galleryFuture;

  @override
  void initState() {
    super.initState();
    galleryFuture = fetchGallery(widget.universityId);
  }

  Future<List<String>> fetchGallery(int id) async {
    try {
      final response =
          await http.get(Uri.parse('${BaseUrl.universityList}$id/'));
      print('🔍 DEBUG: Gallery API Response Status: ${response.statusCode}');

      if (response.statusCode == 200) {
        final data = json.decode(response.body);
        print('🔍 DEBUG: Gallery API Response Data: ${data.toString()}');

        // Check if data has the expected structure
        if (data['success'] == true && data['data'] != null) {
          final universityData = data['data'];

          // Check if gallery exists in the response
          if (universityData['gallery'] != null) {
            final gallery = universityData['gallery'];
            print('🔍 DEBUG: Gallery object found: $gallery');

            // Extract image URLs from the gallery object
            List<String> imageUrls = [];

            // Check each image field (image1 through image6)
            for (int i = 1; i <= 6; i++) {
              final imageKey = 'image${i}_url';
              if (gallery[imageKey] != null &&
                  gallery[imageKey].toString().isNotEmpty) {
                imageUrls.add(gallery[imageKey]);
                print('🔍 DEBUG: Added image$i: ${gallery[imageKey]}');
              }
            }

            print('🔍 DEBUG: Total images found: ${imageUrls.length}');
            return imageUrls;
          } else {
            print('🔍 DEBUG: No gallery found in university data');
            return [];
          }
        } else {
          print('🔍 DEBUG: Invalid API response structure');
          return [];
        }
      } else {
        print(
            '🔍 DEBUG: API request failed with status: ${response.statusCode}');
        throw Exception('Failed to load gallery: HTTP ${response.statusCode}');
      }
    } catch (e) {
      print('🔍 DEBUG: Error fetching gallery: $e');
      throw Exception('Failed to load gallery: $e');
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: cblack10,
      body: FutureBuilder<List<String>>(
        future: galleryFuture,
        builder: (context, snapshot) {
          if (snapshot.connectionState == ConnectionState.waiting) {
            return Center(
              child: CircularProgressIndicator(
                color: Colors.blue,
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
                    'Error loading gallery',
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
                    Icons.photo_library_outlined,
                    color: Colors.grey,
                    size: 48,
                  ),
                  SizedBox(height: 16),
                  Text(
                    'No gallery images available',
                    style: TextStyle(
                      fontSize: 16,
                      fontWeight: FontWeight.bold,
                      color: Colors.grey,
                    ),
                  ),
                  SizedBox(height: 8),
                  Text(
                    'This university has not uploaded any gallery images yet.',
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

          final gallery = snapshot.data!;
          print('🔍 DEBUG: Building gallery with ${gallery.length} images');

          return GridView.builder(
            padding: EdgeInsets.all(16),
            gridDelegate: SliverGridDelegateWithFixedCrossAxisCount(
              crossAxisCount: 2,
              crossAxisSpacing: 10,
              mainAxisSpacing: 10,
              childAspectRatio: 1.0, // Square images
            ),
            itemCount: gallery.length,
            itemBuilder: (context, index) {
              final imageUrl = gallery[index];
              print('🔍 DEBUG: Loading image $index: $imageUrl');

              return ClipRRect(
                borderRadius: BorderRadius.circular(10),
                child: Container(
                  decoration: BoxDecoration(
                    borderRadius: BorderRadius.circular(10),
                    boxShadow: [
                      BoxShadow(
                        color: Colors.black.withOpacity(0.1),
                        blurRadius: 5,
                        offset: Offset(0, 2),
                      ),
                    ],
                  ),
                  child: Image.network(
                    imageUrl,
                    fit: BoxFit.cover,
                    loadingBuilder: (context, child, loadingProgress) {
                      if (loadingProgress == null) {
                        return child;
                      }
                      return Container(
                        decoration: BoxDecoration(
                          color: Colors.grey[200],
                          borderRadius: BorderRadius.circular(10),
                        ),
                        child: Center(
                          child: CircularProgressIndicator(
                            value: loadingProgress.expectedTotalBytes != null
                                ? loadingProgress.cumulativeBytesLoaded /
                                    loadingProgress.expectedTotalBytes!
                                : null,
                            color: Colors.blue,
                          ),
                        ),
                      );
                    },
                    errorBuilder: (context, error, stackTrace) {
                      print('🔍 DEBUG: Error loading image $index: $error');
                      return Container(
                        decoration: BoxDecoration(
                          color: Colors.grey[300],
                          borderRadius: BorderRadius.circular(10),
                        ),
                        child: Center(
                          child: Column(
                            mainAxisAlignment: MainAxisAlignment.center,
                            children: [
                              Icon(
                                Icons.broken_image,
                                color: Colors.grey[600],
                                size: 32,
                              ),
                              SizedBox(height: 8),
                              Text(
                                'Image failed to load',
                                style: TextStyle(
                                  fontSize: 10,
                                  color: Colors.grey[600],
                                ),
                                textAlign: TextAlign.center,
                              ),
                            ],
                          ),
                        ),
                      );
                    },
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
