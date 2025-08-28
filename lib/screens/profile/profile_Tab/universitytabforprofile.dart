import 'dart:convert';
import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;
import 'package:frontend/utils/colors/colors.dart';
import 'package:frontend/_env/env.dart';
import 'package:frontend/widgets/botttom_nav.dart';

class UniversityFavouritesPage extends StatefulWidget {
  const UniversityFavouritesPage({Key? key}) : super(key: key);

  @override
  _UniversityFavouritesPageState createState() =>
      _UniversityFavouritesPageState();
}

class _UniversityFavouritesPageState extends State<UniversityFavouritesPage> {
  List<dynamic> _favourites = [];
  bool _isLoading = true;

  @override
  void initState() {
    super.initState();
    fetchFavourites();
  }

  Future<void> fetchFavourites() async {
    try {
      final response = await http.get(Uri.parse(BaseUrl.favouriteUniversities));

      print("Status code: ${response.statusCode}");
      print("Response body: ${response.body}");

      if (response.statusCode == 200) {
        final Map<String, dynamic> json = jsonDecode(response.body);

        // Check if 'data' exists
        if (json.containsKey('data')) {
          final List<dynamic> data = json['data'];
          setState(() {
            _favourites = data;
          });
        } else {
          print("⚠️ 'data' key not found in JSON");
        }
      } else {
        throw Exception('Failed to load favourites');
      }
    } catch (e) {
      print("Error fetching favourites: $e");
    } finally {
      setState(() {
        _isLoading = false;
      });
    }
  }

  Widget _buildCard(dynamic favItem) {
    final university = favItem['university'];
    final String logoUrl = university['logo_url'] ?? '';
    final String fullImageUrl =
        logoUrl.startsWith('http') ? logoUrl : 'http://localhost:8000/$logoUrl';

    return Card(
      shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(15)),
      elevation: 6,
      margin: const EdgeInsets.symmetric(horizontal: 16, vertical: 10),
      child: Container(
        decoration: BoxDecoration(
          border: Border.all(color: primaryColor.withOpacity(0.5)),
          borderRadius: BorderRadius.circular(15),
        ),
        padding: const EdgeInsets.all(12),
        child: Row(
          children: [
            /// Left: Image (20%)
            Expanded(
              flex: 2,
              child: ClipRRect(
                borderRadius: BorderRadius.circular(12),
                child: Image.network(
                  fullImageUrl,
                  height: 80,
                  width: 80,
                  fit: BoxFit.cover,
                  errorBuilder: (context, error, stackTrace) =>
                      const Icon(Icons.broken_image, size: 50),
                ),
              ),
            ),

            const SizedBox(width: 12),

            /// Middle: Text (60%)
            Expanded(
              flex: 6,
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  Text(
                    university['name'] ?? 'No name',
                    style: const TextStyle(
                      fontSize: 16,
                      fontWeight: FontWeight.bold,
                    ),
                  ),
                  const SizedBox(height: 4),
                  Text(
                    university['city'] ?? 'Unknown location',
                    style: const TextStyle(
                      fontSize: 14,
                      color: Colors.grey,
                    ),
                  ),
                  const SizedBox(height: 4),
                  Text(
                    'Estd. ${university['estd_year'] ?? 'N/A'}',
                    style: const TextStyle(
                      fontSize: 12,
                      color: Colors.black54,
                    ),
                  ),
                ],
              ),
            ),

            /// Right: Love Icon (20%)
            Expanded(
              flex: 2,
              child: Align(
                alignment: Alignment.centerRight,
                child: IconButton(
                  icon: const Icon(Icons.favorite_border, color: Colors.red),
                  onPressed: () {
                    // Handle like button logic
                  },
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
    return Scaffold(
      bottomNavigationBar: BottomButton(
        onTap: () {},
        selectedIndex: 0,
      ),
      body: _isLoading
          ? const Center(child: CircularProgressIndicator())
          : _favourites.isEmpty
              ? const Center(child: Text("No favourites found."))
              : ListView.builder(
                  itemCount: _favourites.length,
                  itemBuilder: (context, index) {
                    return _buildCard(_favourites[index]);
                  },
                ),
    );
  }
}
