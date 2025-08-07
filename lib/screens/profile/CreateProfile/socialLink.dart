import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;
import 'package:frontend/_env/env.dart';
import 'package:frontend/utils/colors/colors.dart';
import 'package:frontend/utils/responsive.dart';
import 'dart:convert'; // Added for jsonEncode

class SocialLink extends StatefulWidget {
  const SocialLink({super.key});

  @override
  _SocialLinkState createState() => _SocialLinkState();
}

class _SocialLinkState extends State<SocialLink> {
  Measurements? size;

  TextEditingController facebookController = TextEditingController();
  TextEditingController linkedInController = TextEditingController();

  Future<void> sendSocialLinks() async {
    final url = BaseUrl.profileSocial;

    try {
      final response = await http.post(
        Uri.parse(url),
        headers: {
          'Content-Type': 'application/json',
        },
        body: jsonEncode({
          'facebook_link': facebookController.text,
          'linkedin_link': linkedInController.text,
        }),
      );

      if (response.statusCode == 200 || response.statusCode == 201) {
        print('Social links sent successfully!');
        // You can add a success toast here
      } else {
        print(
            'Failed to send social links. Status code: ${response.statusCode}');
        print('Response body: ${response.body}');
      }
    } catch (e) {
      print('Error sending social links: $e');
    }
  }

  @override
  Widget build(BuildContext context) {
    size = Measurements(MediaQuery.of(context).size);

    final labelTextStyle = Theme.of(context).textTheme.titleSmall!.copyWith(
          fontSize: 16.0,
          fontWeight: FontWeight.w700,
          fontFamily: 'Roboto',
          // Assuming titlecolor is defined somewhere
          color: titlecolor,
        );

    return Scaffold(
      resizeToAvoidBottomInset: false,
      floatingActionButtonLocation: FloatingActionButtonLocation.centerFloat,
      floatingActionButton: Container(
        height: size?.hp(15),
        margin: const EdgeInsets.all(10),
        child: Align(
          alignment: Alignment.bottomCenter,
          child: Column(
            children: [
              Container(
                width: size?.wp(87),
                height: size?.hp(5),
                decoration: BoxDecoration(
                  color: secondaryColor,
                  borderRadius: BorderRadius.circular(10),
                ),
                child: TextButton(
                  onPressed: () {
                    sendSocialLinks(); // Call the function to send data
                  },
                  child: Text(
                    'Save',
                    textScaleFactor: 1.25,
                    style: TextStyle(
                      fontFamily: 'Roboto',
                      color: thirdColor,
                      fontWeight: FontWeight.w700,
                    ),
                  ),
                ),
              ),
              vGap(20),
              Container(
                width: size?.wp(87),
                height: size?.hp(5),
                decoration: BoxDecoration(
                  color: Colors.white, // Use Colors.white instead of White
                  borderRadius: BorderRadius.circular(10),
                ),
                child: TextButton(
                  onPressed: () {
                    Navigator.pop(context);
                  },
                  child: Text(
                    'Cancel',
                    textScaleFactor: 1.25,
                    style: TextStyle(
                      fontFamily: 'Roboto',
                      color: Colors.black,
                      fontWeight: FontWeight.w700,
                    ),
                  ),
                ),
              ),
            ],
          ),
        ),
      ),
      backgroundColor: cblack10,
      appBar: AppBar(
        elevation: 1,
        leading: IconButton(
          onPressed: () {
            Navigator.pop(context);
          },
          icon: Icon(
            Icons.arrow_back_ios,
            color: Colors.black,
          ),
        ),
        backgroundColor: Colors.white, // Use Colors.white instead of whiteColor
        title: Text(
          "Social Links",
          style: labelTextStyle,
        ),
      ),
      body: Padding(
        padding: const EdgeInsets.only(top: 18.0, left: 8, right: 8),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Text(
              "Facebook",
              style: labelTextStyle,
            ),
            vGap(10),
            TextField(
              controller: facebookController,
              decoration: InputDecoration(
                border: OutlineInputBorder(),
                labelText: 'Enter Your Link',
                hintText: 'Enter your link',
              ),
            ),
            vGap(20),
            Text(
              "LinkedIn",
              style: labelTextStyle,
            ),
            vGap(10),
            TextField(
              controller: linkedInController,
              decoration: InputDecoration(
                border: OutlineInputBorder(),
                labelText: 'Enter Your Link',
                hintText: 'Enter your link',
              ),
            ),
          ],
        ),
      ),
    );
  }
}
