import 'dart:convert';
import 'package:flutter/material.dart';
import 'package:frontend/utils/BottomNavigation/bottom_navigation.dart';
import 'package:http/http.dart' as http;
import 'package:frontend/utils/colors/colors.dart';
import 'package:frontend/_env/env.dart';
import 'package:frontend/widgets/botttom_nav.dart';

class MCQNotesScreen extends StatefulWidget {
  const MCQNotesScreen({super.key});

  @override
  _MCQNotesScreenState createState() => _MCQNotesScreenState();
}

class _MCQNotesScreenState extends State<MCQNotesScreen> {
  late Future<List<Map<String, dynamic>>> modulesFuture;
  int _selectedIndex = 3; // Notes tab is active

  @override
  void initState() {
    super.initState();
    modulesFuture = fetchMCQModules();
  }

  /// Fetch all MCQs and group by module
  Future<List<Map<String, dynamic>>> fetchMCQModules() async {
    try {
      final response = await http.get(
        Uri.parse('${BaseUrl.baseUrl}/notes/notesmcqs/'),
        headers: {
          'Content-Type': 'application/json',
          'Accept': 'application/json',
        },
      );

      if (response.statusCode == 200) {
        final data = json.decode(response.body);
        final List<dynamic> mcqs = data['data'];

        // Group MCQs by module_title
        Map<String, Map<String, dynamic>> modulesMap = {};

        for (var mcq in mcqs) {
          String title = mcq['module_title'] ?? 'Unknown Module';
          if (modulesMap.containsKey(title)) {
            modulesMap[title]!['mcq_count'] += 1;
          } else {
            modulesMap[title] = {
              'module_title': title,
              'module_description': mcq['module_description'] ?? '',
              'mcq_count': 1,
            };
          }
        }

        return modulesMap.values.toList();
      } else {
        print('❌ API Error: ${response.statusCode}');
        return [];
      }
    } catch (e) {
      print('❌ Error fetching MCQ modules: $e');
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
                '${module['mcq_count']} MCQs',
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

  /// Bottom navigation

  @override
  Widget build(BuildContext context) {
    return Scaffold(
        backgroundColor: color3,
        appBar: AppBar(
          backgroundColor: primaryColor,
          title: Text(
            'MCQ Modules',
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
                return Center(child: Text('Failed to load MCQ modules'));
              }

              final modules = snapshot.data ?? [];
              if (modules.isEmpty) {
                return Center(child: Text('No MCQ modules found'));
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
        bottomNavigationBar: BottomButton(onTap: () {}, selectedIndex: 3));
  }
}
