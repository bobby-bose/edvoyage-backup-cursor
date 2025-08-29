import 'dart:convert';
import 'package:flutter/material.dart';
import 'package:frontend/utils/BottomNavigation/bottom_navigation.dart';
import 'package:http/http.dart' as http;
import 'package:frontend/utils/colors/colors.dart';
import 'package:frontend/_env/env.dart';
import 'package:frontend/widgets/botttom_nav.dart';

class ClinicalCasesScreen extends StatefulWidget {
  const ClinicalCasesScreen({super.key});

  @override
  _ClinicalCasesScreenState createState() => _ClinicalCasesScreenState();
}

class _ClinicalCasesScreenState extends State<ClinicalCasesScreen> {
  late Future<List<Map<String, dynamic>>> modulesFuture;
  int _selectedIndex = 3; // Notes tab is active

  @override
  void initState() {
    super.initState();
    modulesFuture = fetchClinicalModules();
  }

  /// Fetch clinical case modules
  Future<List<Map<String, dynamic>>> fetchClinicalModules() async {
    try {
      final response = await http.get(
        Uri.parse('${BaseUrl.baseUrl}/notes/notesclinicalcases/'),
        headers: {
          'Content-Type': 'application/json',
          'Accept': 'application/json',
        },
      );

      if (response.statusCode == 200) {
        final data = json.decode(response.body);
        final List<dynamic> modules = data['data'];

        return modules
            .map<Map<String, dynamic>>((item) => item as Map<String, dynamic>)
            .toList();
      } else {
        print('❌ API Error: ${response.statusCode}');
        return [];
      }
    } catch (e) {
      print('❌ Error fetching clinical modules: $e');
      return [];
    }
  }

  /// Build individual module cards
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
                '${module['clinical_cases_count']} Case(s)',
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
          'Clinical Case Modules',
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
              return Center(
                  child: Text('Failed to load clinical case modules'));
            }

            final modules = snapshot.data ?? [];
            if (modules.isEmpty) {
              return Center(child: Text('No Clinical Case modules found'));
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
