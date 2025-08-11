import 'package:flutter/material.dart';
import 'package:frontend/screens/timer/main.dart';
import 'package:frontend/widgets/botttom_nav.dart';

class StudyAbroadScreen extends StatefulWidget {
  const StudyAbroadScreen({super.key});

  @override
  _StudyAbroadScreenState createState() => _StudyAbroadScreenState();
}

class _StudyAbroadScreenState extends State<StudyAbroadScreen> {
  @override
  Widget build(BuildContext context) {
    final size = MediaQuery.of(context).size;

    return Scaffold(
      backgroundColor: Colors.white,
      body: SafeArea(
        child: Column(
          children: [
            // Header Section
            _buildHeader(),

            // Main Content
            Expanded(
              child: SingleChildScrollView(
                padding: EdgeInsets.symmetric(horizontal: 24, vertical: 16),
                child: Column(
                  children: [
                    // Hero Graphic Section
                    _buildHeroGraphic(),

                    SizedBox(height: 24),

                    // Content Block
                    _buildContentBlock(),

                    SizedBox(height: 32),

                    // Action Button
                    _buildActionButton(),

                    SizedBox(height: 24),
                  ],
                ),
              ),
            ),
          ],
        ),
      ),
      bottomNavigationBar:
          BottomButton(onTap: () {}, selectedIndex: 4), // Study Abroad tab
    );
  }

  /// Builds the header section with title and border separator
  Widget _buildHeader() {
    return Container(
      padding: EdgeInsets.symmetric(horizontal: 24, vertical: 20),
      decoration: BoxDecoration(
        color: Colors.white,
        border: Border(
          bottom: BorderSide(
            color: Color(0xFFE0E0E0),
            width: 1,
          ),
        ),
      ),
      child: Column(
        children: [
          Text(
            'Study Abroad',
            style: TextStyle(
              fontSize: 28,
              fontWeight: FontWeight.bold,
              color: Color(0xFF005F55),
              fontFamily: 'Poppins',
            ),
            textAlign: TextAlign.center,
          ),
        ],
      ),
    );
  }

  /// Builds the hero graphic section with illustration
  Widget _buildHeroGraphic() {
    return SizedBox(
      height: MediaQuery.of(context).size.height * 0.35, // 35% of screen height
      child: Center(
        child: Image.asset(
          'assets/overseas1.png',
          height: 300,
          width: 300,
        ),
      ),
    );
  }

  /// Builds the content block with subtitle and bullet points
  Widget _buildContentBlock() {
    return Column(
      children: [
        // Subtitle
        Text(
          'Overseas Study Expert',
          style: TextStyle(
            fontSize: 20,
            fontWeight: FontWeight.bold,
            color: Color(0xFF00796B),
            fontFamily: 'Poppins',
          ),
          textAlign: TextAlign.center,
        ),

        SizedBox(height: 24),

        // Bullet Points
        _buildBulletPoint('Planning to study MBBS abroad?'),
        SizedBox(height: 12),
        _buildBulletPoint(
            'But unsure which university would be the best-fit for you?'),
        SizedBox(height: 12),
        _buildBulletPoint(
            'Devoyage experts will guide on every step in your journey.'),
        SizedBox(height: 12),
        _buildBulletPoint(
            'Start with our course finder and schedule a slot with a counsellor.'),
      ],
    );
  }

  /// Builds individual bullet point
  Widget _buildBulletPoint(String text) {
    return SizedBox(
      width: MediaQuery.of(context).size.width * 0.8,
      child: Row(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Container(
            margin: EdgeInsets.only(top: 8, right: 12),
            width: 6,
            height: 6,
            decoration: BoxDecoration(
              color: Color(0xFF444444),
              shape: BoxShape.circle,
            ),
          ),
          Expanded(
            child: Text(
              text,
              style: TextStyle(
                fontSize: 16,
                color: Color(0xFF444444),
                height: 1.5,
                fontFamily: 'Poppins',
              ),
            ),
          ),
        ],
      ),
    );
  }

  /// Builds the action button
  Widget _buildActionButton() {
    return SizedBox(
      width: MediaQuery.of(context).size.width * 0.6,
      child: ElevatedButton(
        onPressed: () {
          // TODO: Navigate to course finder or slot booking screen
          Navigator.push(
            context,
            MaterialPageRoute(builder: (context) => TimerScreen()),
          );
        },
        style: ElevatedButton.styleFrom(
          backgroundColor: Color(0xFFFF5E5B), // Coral red
          foregroundColor: Colors.white,
          padding: EdgeInsets.symmetric(horizontal: 32, vertical: 14),
          shape: RoundedRectangleBorder(
            borderRadius: BorderRadius.circular(8),
          ),
          elevation: 2,
        ),
        child: Text(
          'Begin',
          style: TextStyle(
            fontSize: 16,
            fontWeight: FontWeight.bold,
            fontFamily: 'Poppins',
          ),
        ),
      ),
    );
  }
}
