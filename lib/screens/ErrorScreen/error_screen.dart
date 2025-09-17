import 'package:flutter/material.dart';

import 'package:frontend/utils/colors/colors.dart';
import 'package:frontend/utils/responsive.dart';

class ErrorScreen extends StatefulWidget {
  const ErrorScreen({super.key});

  @override
  _ErrorScreenState createState() => _ErrorScreenState();
}

final style = TextStyle(
    fontFamily: 'Roboto',
    fontSize: 16,
    fontWeight: FontWeight.w600,
    color: Colors.black);

class _ErrorScreenState extends State<ErrorScreen> {
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: White,
      appBar: AppBar(
        backgroundColor: Colors.white,
        elevation: 1,
        centerTitle: true,
        title: RichText(
          text: TextSpan(
            children: <TextSpan>[
              TextSpan(
                  text: 'edvo',
                  style: TextStyle(
                      fontFamily: 'Roboto',
                      letterSpacing: 1,
                      fontWeight: FontWeight.bold,
                      fontSize: 26,
                      color: primaryColor)),
              TextSpan(
                  text: 'y',
                  style: TextStyle(
                      fontFamily: 'Roboto',
                      fontWeight: FontWeight.bold,
                      fontSize: 26,
                      color: secondaryColor)),
              TextSpan(
                  text: 'age',
                  style: TextStyle(
                      fontFamily: 'Roboto',
                      letterSpacing: 1,
                      fontWeight: FontWeight.bold,
                      fontSize: 26,
                      color: primaryColor)),
            ],
          ),
        ),
      ),
      body: Center(
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.center,
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            SizedBox(
                width: getWidth(context),
                child: Image.asset(
                  "assets/3793096 1.png",
                  fit: BoxFit.cover,
                )),
            Text(
              "Oopss,You’ve Lost In Space",
              style: TextStyle(fontSize: 18, fontWeight: FontWeight.w700),
            ),
            vGap(10),
            Text(
              "We can’t finding the page you looking for",
              style: TextStyle(fontSize: 12, fontWeight: FontWeight.w500),
            ),
            vGap(50),
            Padding(
              padding: const EdgeInsets.all(18.0),
              child: ElevatedButton(
                  onPressed: () {},
                  style: ElevatedButton.styleFrom(
                    backgroundColor: secondaryColor,
                    shadowColor: secondaryColor,
                    elevation: 5,
                    shape: RoundedRectangleBorder(
                      borderRadius: BorderRadius.circular(15.0),
                    ),
                  ),
                  child: Text(
                    'Try Again',
                    style: TextStyle(
                      fontFamily: 'Roboto',
                    ),
                  )),
            )
          ],
        ),
      ),
    );
  }
}
