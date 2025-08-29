import 'dart:convert';
import 'package:flutter/material.dart';
import 'package:frontend/utils/BottomNavigation/bottom_navigation.dart';
import 'package:http/http.dart' as http;
import 'package:frontend/utils/colors/colors.dart';
import 'package:frontend/_env/env.dart';
import 'package:frontend/widgets/botttom_nav.dart';

class FlashCardModulesScreen extends StatefulWidget {
  const FlashCardModulesScreen({super.key});

  @override
  _FlashCardModulesScreenState createState() => _FlashCardModulesScreenState();
}

class _FlashCardModulesScreenState extends State<FlashCardModulesScreen> {
  late Future<List<Map<String, dynamic>>> modulesFuture;
  int _selectedIndex = 3; // Notes tab is active

  @override
  void initState() {
    super.initState();
    modulesFuture = fetchFlashCardModules();
  }

  /// Fetch all flash cards and group by module
  Future<List<Map<String, dynamic>>> fetchFlashCardModules() async {
    try {
      final response = await http.get(
        Uri.parse('${BaseUrl.baseUrl}/notes/notesflashcards/'),
        headers: {
          'Content-Type': 'application/json',
          'Accept': 'application/json',
        },
      );

      if (response.statusCode == 200) {
        final data = json.decode(response.body);
        final List<dynamic> modulesData = data['data'];

        return modulesData.map<Map<String, dynamic>>((module) {
          return {
            'module_id': module['module_id'],
            'module_title': module['module_title'],
            'module_description': module['module_description'],
            'flash_cards_count': module['flash_cards_count'],
          };
        }).toList();
      } else {
        print('❌ API Error: ${response.statusCode}');
        return [];
      }
    } catch (e) {
      print('❌ Error fetching flash card modules: $e');
      return [];
    }
  }

  /// Builds individual module cards
  Widget _buildModuleCard(Map<String, dynamic> module) {
    return Container(
      margin: EdgeInsets.symmetric(horizontal: 20, vertical: 8),
      padding: EdgeInsets.symmetric(horizontal: 16, vertical: 12),
      decoration: BoxDecoration(
        color: whiteColor,
        borderRadius: BorderRadius.circular(8),
        border: Border(
          bottom: BorderSide(color: grey1, width: 1),
        ),
      ),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Text(
            module['module_title'] ?? 'Unknown Module',
            style: TextStyle(
              fontFamily: 'Poppins',
              fontSize: 16,
              fontWeight: FontWeight.bold,
              color: titlecolor,
            ),
          ),
          SizedBox(height: 4),
          Text(
            module['module_description'] ?? '',
            style: TextStyle(
              fontFamily: 'Poppins',
              fontSize: 14,
              color: grey3,
            ),
          ),
          SizedBox(height: 8),
          Row(
            children: [
              Spacer(),
              Text(
                '${module['flash_cards_count']} Flash Cards',
                style: TextStyle(
                  fontFamily: 'Poppins',
                  fontSize: 14,
                  color: grey3,
                  fontWeight: FontWeight.w500,
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
        backgroundColor: primaryColor,
        title: Text(
          'Flash Card Modules',
          style: TextStyle(
            fontFamily: 'Poppins',
            fontSize: 20,
            fontWeight: FontWeight.bold,
            color: whiteColor,
          ),
        ),
        centerTitle: true,
        elevation: 0,
      ),
      body: SafeArea(
        child: FutureBuilder<List<Map<String, dynamic>>>(
          future: modulesFuture,
          builder: (context, snapshot) {
            if (snapshot.connectionState == ConnectionState.waiting) {
              return Center(
                child: CircularProgressIndicator(color: primaryColor),
              );
            }

            if (snapshot.hasError) {
              return Center(child: Text('Failed to load Flash Card modules'));
            }

            final modules = snapshot.data ?? [];
            if (modules.isEmpty) {
              return Center(child: Text('No Flash Card modules found'));
            }

            return ListView.builder(
              padding: EdgeInsets.symmetric(vertical: 8),
              itemCount: modules.length,
              itemBuilder: (context, index) {
                return _buildModuleCard(modules[index]);
              },
            );
          },
        ),
      ),
      bottomNavigationBar: BottomButton(onTap: () {}, selectedIndex: 3),
    );
  }
}
