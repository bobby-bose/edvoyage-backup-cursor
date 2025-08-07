import 'package:flutter/material.dart';
import 'package:frontend/utils/colors/colors.dart';
import 'package:frontend/widgets/botttom_nav.dart';

class FlashCardNotesScreen extends StatefulWidget {
  const FlashCardNotesScreen({super.key});

  @override
  _FlashCardNotesScreenState createState() => _FlashCardNotesScreenState();
}

class _FlashCardNotesScreenState extends State<FlashCardNotesScreen> {
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: color3,
      appBar: AppBar(
        backgroundColor: primaryColor,
        title: Text(
          'Flash Cards',
          style: TextStyle(
            fontFamily: 'Poppins',
            fontSize: 20,
            fontWeight: FontWeight.w600,
            color: whiteColor,
          ),
        ),
        centerTitle: true,
        elevation: 0,
        leading: IconButton(
          icon: Icon(Icons.arrow_back_ios, color: whiteColor),
          onPressed: () {
            Navigator.pop(context);
          },
        ),
      ),
      body: Center(
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            Icon(
              Icons.flash_on,
              size: 64,
              color: primaryColor,
            ),
            SizedBox(height: 16),
            Text(
              'Flash Cards Coming Soon',
              style: TextStyle(
                fontFamily: 'Poppins',
                fontSize: 20,
                fontWeight: FontWeight.w600,
                color: titlecolor,
              ),
            ),
            SizedBox(height: 8),
            Text(
              'This feature is under development',
              style: TextStyle(
                fontFamily: 'Poppins',
                fontSize: 14,
                color: grey3,
              ),
            ),
          ],
        ),
      ),
      bottomNavigationBar: BottomButton(onTap: () {}, selectedIndex: 3),
    );
  }
}
