import 'package:flutter/material.dart';
import '../../utils/avatar.dart';
import '../../utils/colors/colors.dart';
import '../../utils/responsive.dart';

class terms_condition extends StatefulWidget {
  const terms_condition({super.key});

  @override
  State<terms_condition> createState() => _terms_conditionState();
}

class _terms_conditionState extends State<terms_condition> {
  Measurements? size;

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: Padding(
        padding: const EdgeInsets.all(20),
        child: Column(
          mainAxisAlignment: MainAxisAlignment.start,
          children: [
            Stack(
              children: [
                SizedBox(
                  height: MediaQuery.of(context).size.height *
                      0.2, // 30% of the screen height
                  width: MediaQuery.of(context).size.width * 0.9,
                  child: Image.asset(
                      edvoyagelogo1), // Replace with your image path
                ),
                Positioned(
                  bottom: 10, // Adjust the position as needed
                  left: 70, // Adjust the position as needed
                  child: Text(
                    'TERMS & CONDITIONS',
                    textScaleFactor: 1.1,
                    style: TextStyle(
                      color: primaryColor,
                      fontFamily: 'Roboto',
                      fontSize: 20,
                      fontWeight: FontWeight.w600,
                    ),
                  ),
                ),
              ],
            ),
            SizedBox(
              height: 10,
            ),
            Text(
              'Welcome to Website Name These terms and conditions outline the rules and regulations for the use of Company Names Website,'
              ' located at WebsiteBy accessing this website we assume you accept these terms and conditions. Do not continue to use Website Name '
              'if you do not agree to take all of the terms and conditions stated on this page.The following terminology applies to these Terms and Conditions,'
              ' Privacy Statement and Disclaimer Notice and all Agreements: Client, You and Your refers to you, the person log on this website and compliant '
              'to the Company terms and conditions. “The Company”, “Ourselves”, “We”, “Our” and “Us”, refers to our Company. “Party”, “Parties”, or “Us”, '
              'refers to both the Client and ourselves. '
              'All terms refer to the offer, acceptance and consideration of payment necessary to undertake the '
              'process of our assistance to the Client in the most appropriate manner for the express purpose of '
              'meeting the Client needs in respect of provision of the Company stated services, in accordance with '
              'and subject to, prevailing law of Netherlands. Any use of the above terminology or other words in the'
              ' singular, plural, capitalization and/or he/she or they, are taken as interchangeable and therefore as'
              ' referring to same.Welcome to Website Name These terms and conditions outline the rules and regulations for the use of Company Names Website,'
              ' located at WebsiteBy accessing this website we assume you accept these terms and conditions. Do not continue to use Website Name '
              'if you do not agree to take all of the terms and conditions stated on this page.The following terminology applies to these Terms and Conditions,'
              ' Privacy Statement and Disclaimer Notice and all Agreements: Client, You and Your refers to you, the person log on this website and compliant '
              'to the Company terms and conditions. “The Company”, “Ourselves”, “We”, “Our” and “Us”, refers to our Company. “Party”, “Parties”, or “Us”, '
              'refers to both the Client and ourselves. '
              'All terms refer to the offer, acceptance and consideration of payment necessary to undertake the '
              'process of our assistance to the Client in the most appropriate manner for the express purpose of '
              'meeting the Client needs in respect of provision of the Company stated services, in accordance with '
              'and subject to, prevailing law of Netherlands. Any use of the above terminology or other words in the'
              ' singular, plural, capitalization and/or he/she or they, are taken as interchangeable and therefore as'
              ' referring to same.',
              style: TextStyle(
                color: primaryColor,
                fontFamily: 'Roboto',
                fontSize: 14,
                fontWeight: FontWeight.w600,
              ),
            )
          ],
        ),
      ),
    );
  }
}
