import 'package:flutter/material.dart';
import 'package:frontend/utils/colors/colors.dart';
import 'package:frontend/utils/responsive.dart';
import '../CreateProfile/education_details.dart';
import '../CreateProfile/socialLink.dart';
import '../CreateProfile/workDetails.dart';

class ProfileAbout extends StatefulWidget {
  const ProfileAbout({super.key});

  @override
  _ProfileAboutState createState() => _ProfileAboutState();
}

final style = TextStyle(
    fontFamily: 'Roboto',
    fontSize: 16,
    fontWeight: FontWeight.w600,
    color: Colors.black);

class _ProfileAboutState extends State<ProfileAbout> {
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: color3,
      body: SingleChildScrollView(
        child: Column(
          children: [
            Padding(
              padding: const EdgeInsets.all(10.0),
              child: Column(
                children: [
                  Row(
                    mainAxisAlignment: MainAxisAlignment.spaceBetween,
                    children: [
                      Text("Education", style: style),
                      TextButton(
                        onPressed: () {
                          Navigator.push(
                              context,
                              MaterialPageRoute(
                                  builder: ((context) => EducationDetails())));
                        },
                        child: Icon(
                          Icons.add,
                          size: 32,
                          color: secondaryColor,
                        ),
                      ),
                    ],
                  ),
                  Row(
                    mainAxisAlignment: MainAxisAlignment.spaceBetween,
                    children: [
                      Text(
                        "Working",
                        style: style,
                      ),
                      TextButton(
                        onPressed: () {
                          Navigator.push(
                              context,
                              MaterialPageRoute(
                                  builder: ((context) => WorkDetails())));
                        },
                        child: Icon(
                          Icons.add,
                          size: 32,
                          color: secondaryColor,
                        ),
                      ),
                    ],
                  ),
                  Row(
                    mainAxisAlignment: MainAxisAlignment.spaceBetween,
                    children: [
                      Text(
                        "Social Links",
                        style: style,
                      ),
                      TextButton(
                        onPressed: () {
                          Navigator.push(
                              context,
                              MaterialPageRoute(
                                  builder: ((context) => SocialLink())));
                        },
                        child: Icon(
                          Icons.add,
                          size: 32,
                          color: secondaryColor,
                        ),
                      ),
                    ],
                  )
                ],
              ),
            ),
            vGap(20),
          ],
        ),
      ),
    );
  }
}
