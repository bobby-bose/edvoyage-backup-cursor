import 'package:flutter/material.dart';
import 'package:fluttertoast/fluttertoast.dart';
import 'package:google_fonts/google_fonts.dart';

import '../../utils/avatar.dart';
import '../../utils/colors/colors.dart';

class sooon extends StatefulWidget {
  const sooon({super.key});

  @override
  State<sooon> createState() => _sooonState();
}

class _sooonState extends State<sooon> {
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        backgroundColor: Colors.white,
        elevation: 0.3, // You can adjust the elevation as needed
        centerTitle: true,
        title: SizedBox(
          height: 200, // Set the height of the container
          child:
              Image.asset(edvoyagelogo1), // Replace with the actual image path
        ),
      ),
      body: Column(
        mainAxisAlignment: MainAxisAlignment.center,
        children: [
          Container(
            alignment: Alignment.center,
            child: Image.asset(soon),
          ),
          SizedBox(
            height: 20,
          ),
          Text(
            'COMING  SOON!!!!...',
            style: GoogleFonts.jost(
                letterSpacing: 3,
                fontSize: 27,
                fontWeight: FontWeight.w500,
                color: Colors.black),
          ),
          SizedBox(
            height: 15,
          ),
          ElevatedButton(
            onPressed: () {
              Fluttertoast.showToast(
                msg: 'You will be notify through SMS', // Your message here
                toastLength: Toast.LENGTH_SHORT, // Duration of the message
                gravity: ToastGravity
                    .BOTTOM, // Location of the message on the screen
                backgroundColor:
                    Colors.black.withOpacity(0.7), // Background color
                textColor: Colors.white, // Text color
              );
            },
            style: ElevatedButton.styleFrom(
              foregroundColor: primaryColor,
              shape: RoundedRectangleBorder(
                borderRadius:
                    BorderRadius.circular(10), // Button's border radius
              ),
              textStyle: TextStyle(
                fontSize: 16, // Text font size
                fontWeight: FontWeight.bold, // Text font weight
              ),
            ),
            child: Text('NOTIFY ME'), // Text displayed on the button
          )
        ],
      ),
    );
  }
}
