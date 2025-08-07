import 'package:flutter/material.dart';
import 'package:flutter/services.dart';
import 'package:frontend/_env/env.dart';
import 'package:frontend/utils/Toasty.dart';
import 'package:http/http.dart' as http;
import 'package:frontend/utils/colors/colors.dart';
import 'package:frontend/utils/responsive.dart';
import 'dart:convert'; // Added for jsonEncode
import 'dart:io'; // Added for SocketException
import 'dart:async'; // Added for TimeoutException

class EducationDetails extends StatefulWidget {
  const EducationDetails({super.key});

  @override
  _EducationDetailsState createState() => _EducationDetailsState();
}

class _EducationDetailsState extends State<EducationDetails> {
  Measurements? size;
  String? dropdownValueStartYearHigher;
  String? dropdownValueEndYearHigher;
  TextEditingController gradeControllerHigher = TextEditingController();

  String? dropdownValueStartYearSecondary;
  String? dropdownValueEndYearSecondary;
  TextEditingController gradeControllerSecondary = TextEditingController();

  final _formKey = GlobalKey<FormState>();
  final bool _checkbox = false;
  List<String> years = List.generate(
      66, (index) => (1960 + index).toString()); // 1960 to 2025 as strings

  Future<void> sendDataToBackend() async {
    final url = BaseUrl.profileEducation;
    print('Attempting to connect to: $url');

    try {
      // Validate required fields for Higher Education
      if (dropdownValueStartYearHigher == null ||
          dropdownValueStartYearHigher!.isEmpty) {
        Toasty.showtoast('Please select a start year for higher education');
        return;
      }

      if (dropdownValueEndYearHigher == null ||
          dropdownValueEndYearHigher!.isEmpty) {
        Toasty.showtoast('Please select an end year for higher education');
        return;
      }

      // Validate required fields for Secondary Education
      if (dropdownValueStartYearSecondary == null ||
          dropdownValueStartYearSecondary!.isEmpty) {
        Toasty.showtoast('Please select a start year for secondary education');
        return;
      }

      if (dropdownValueEndYearSecondary == null ||
          dropdownValueEndYearSecondary!.isEmpty) {
        Toasty.showtoast('Please select an end year for secondary education');
        return;
      }

      // Validate GPA format for Higher Education
      double? higherGpaValue;
      if (gradeControllerHigher.text.isNotEmpty) {
        try {
          higherGpaValue = double.parse(gradeControllerHigher.text);
          if (higherGpaValue < 0 || higherGpaValue > 5) {
            Toasty.showtoast('Higher Education GPA must be between 0 and 5');
            return;
          }
        } catch (e) {
          Toasty.showtoast(
              'Please enter a valid GPA for Higher Education (e.g., 3.75)');
          return;
        }
      }

      // Validate GPA format for Secondary Education
      double? secondaryGpaValue;
      if (gradeControllerSecondary.text.isNotEmpty) {
        try {
          secondaryGpaValue = double.parse(gradeControllerSecondary.text);
          if (secondaryGpaValue < 0 || secondaryGpaValue > 5) {
            Toasty.showtoast('Secondary Education GPA must be between 0 and 5');
            return;
          }
        } catch (e) {
          Toasty.showtoast(
              'Please enter a valid GPA for Secondary Education (e.g., 3.75)');
          return;
        }
      }

      // Prepare data for simple education API
      final educationData = {
        'higher_start_year': int.parse(dropdownValueStartYearHigher!),
        'higher_end_year': int.parse(dropdownValueEndYearHigher!),
        'higher_gpa': higherGpaValue,
        'lower_start_year': int.parse(dropdownValueStartYearSecondary!),
        'lower_end_year': int.parse(dropdownValueEndYearSecondary!),
        'lower_gpa': secondaryGpaValue,
      };

      print('Education Request body: $educationData');

      final response = await http
          .post(
            Uri.parse(url),
            headers: {
              'Content-Type': 'application/json',
            },
            body: jsonEncode(educationData),
          )
          .timeout(Duration(seconds: 10));

      print('Response status: ${response.statusCode}');
      print('Response body: ${response.body}');

      if (response.statusCode == 200 || response.statusCode == 201) {
        print('Education data saved successfully!');
        Toasty.showtoast('Education data saved successfully!');
      } else {
        print('Failed to send data. Status: ${response.statusCode}');
        Toasty.showtoast('Failed to save education data. Please try again.');
      }
    } on SocketException catch (e) {
      print('Network error: $e');
      Toasty.showtoast(
          'Network error: Check your internet connection and server IP');
    } on TimeoutException catch (e) {
      print('Timeout error: $e');
      Toasty.showtoast('Request timeout: Server not responding');
    } catch (error) {
      print('Error sending data: $error');
      Toasty.showtoast('Error sending data: $error');
    }
  }

  @override
  Widget build(BuildContext context) {
    size = Measurements(MediaQuery.of(context).size);

    final labelTextStyle = Theme.of(context).textTheme.titleSmall!.copyWith(
          fontSize: 16.0,
          fontWeight: FontWeight.w700,
          fontFamily: 'Roboto',
          color: titlecolor,
        );

    return Scaffold(
      resizeToAvoidBottomInset: false,
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
        backgroundColor: whiteColor,
        title: Text(
          "Educational Details",
          style: labelTextStyle,
        ),
      ),
      body: Padding(
        padding: const EdgeInsets.only(top: 18.0, left: 8, right: 8),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            vGap(10),
            Text(
              "Higher Education",
              style: TextStyle(
                  fontFamily: 'Roboto',
                  fontSize: 16.0,
                  fontWeight: FontWeight.w700,
                  color: secondaryColor),
            ),
            vGap(10),
            Padding(
              padding: const EdgeInsets.all(8.0),
              child: Container(
                decoration: BoxDecoration(
                  borderRadius: BorderRadius.all(Radius.circular(10)),
                  border: Border.all(color: Colors.black),
                  color: White,
                ),
                child: Center(
                  child: DropdownButton<String>(
                    underline: SizedBox(),
                    hint: Text("--Start Year--"),
                    value: dropdownValueStartYearHigher,
                    onChanged: (String? newValue) {
                      setState(() {
                        dropdownValueStartYearHigher = newValue!;
                      });
                    },
                    items: years.map<DropdownMenuItem<String>>((String value) {
                      return DropdownMenuItem<String>(
                        value: value,
                        child: Text(
                          value,
                        ),
                      );
                    }).toList(),
                  ),
                ),
              ),
            ),
            vGap(20),
            Padding(
              padding: const EdgeInsets.all(8.0),
              child: Container(
                decoration: BoxDecoration(
                  borderRadius: BorderRadius.all(Radius.circular(10)),
                  border: Border.all(color: Colors.black),
                  color: White,
                ),
                child: Center(
                  child: DropdownButton<String>(
                    underline: SizedBox(),
                    hint: Text("--End Year--"),
                    value: dropdownValueEndYearHigher,
                    onChanged: (String? newValue) {
                      setState(() {
                        dropdownValueEndYearHigher = newValue!;
                      });
                    },
                    items: years.map<DropdownMenuItem<String>>((String value) {
                      return DropdownMenuItem<String>(
                        value: value,
                        child: Text(
                          value,
                        ),
                      );
                    }).toList(),
                  ),
                ),
              ),
            ),
            Row(
              mainAxisAlignment: MainAxisAlignment.spaceBetween,
              children: [
                Expanded(
                  child: Padding(
                    padding: const EdgeInsets.all(8.0),
                    child: Container(
                      decoration: BoxDecoration(
                        borderRadius: BorderRadius.all(Radius.circular(10)),
                        color: White,
                      ),
                      child: TextField(
                        controller: gradeControllerHigher,
                        keyboardType: TextInputType.number,
                        inputFormatters: [
                          FilteringTextInputFormatter.allow(
                              RegExp(r'[a-zA-Z0-9\s\-\.]')),
                        ],
                        decoration: InputDecoration(
                          border: OutlineInputBorder(),
                          labelText: 'Enter Grade(%)',
                          hintText: 'Enter Grade(%)',
                        ),
                      ),
                    ),
                  ),
                ),
                Expanded(
                  child: Padding(
                      padding: const EdgeInsets.all(8.0),
                      child: Text("(Visible only to user)")),
                )
              ],
            ),
            Divider(
              thickness: 1,
            ),
            vGap(10),
            Text(
              "Secondary Education",
              style: TextStyle(
                  fontSize: 16.0,
                  fontFamily: 'Roboto',
                  fontWeight: FontWeight.w700,
                  color: secondaryColor),
            ),
            vGap(10),
            Padding(
              padding: const EdgeInsets.all(8.0),
              child: Container(
                decoration: BoxDecoration(
                  borderRadius: BorderRadius.all(Radius.circular(10)),
                  border: Border.all(color: Colors.black),
                  color: White,
                ),
                child: Center(
                  child: DropdownButton<String>(
                    underline: SizedBox(),
                    hint: Text("--Start Year--"),
                    value: dropdownValueStartYearSecondary,
                    onChanged: (String? newValue) {
                      setState(() {
                        dropdownValueStartYearSecondary = newValue!;
                      });
                    },
                    items: years.map<DropdownMenuItem<String>>((String value) {
                      return DropdownMenuItem<String>(
                        value: value,
                        child: Text(
                          value,
                        ),
                      );
                    }).toList(),
                  ),
                ),
              ),
            ),
            vGap(20),
            Padding(
              padding: const EdgeInsets.all(8.0),
              child: Container(
                decoration: BoxDecoration(
                  borderRadius: BorderRadius.all(Radius.circular(10)),
                  border: Border.all(color: Colors.black),
                  color: White,
                ),
                child: Center(
                  child: DropdownButton<String>(
                    underline: SizedBox(),
                    hint: Text("--End Year--"),
                    value: dropdownValueEndYearSecondary,
                    onChanged: (String? newValue) {
                      setState(() {
                        dropdownValueEndYearSecondary = newValue!;
                      });
                    },
                    items: years.map<DropdownMenuItem<String>>((String value) {
                      return DropdownMenuItem<String>(
                        value: value,
                        child: Text(
                          value,
                        ),
                      );
                    }).toList(),
                  ),
                ),
              ),
            ),
            Row(
              mainAxisAlignment: MainAxisAlignment.spaceBetween,
              children: [
                Expanded(
                  child: Padding(
                    padding: const EdgeInsets.all(8.0),
                    child: Container(
                      decoration: BoxDecoration(
                        borderRadius: BorderRadius.all(Radius.circular(10)),
                        color: White,
                      ),
                      child: TextField(
                        controller: gradeControllerSecondary,
                        keyboardType: TextInputType.number,
                        inputFormatters: [
                          FilteringTextInputFormatter.allow(
                              RegExp(r'[a-zA-Z0-9\s\-\.]')),
                        ],
                        decoration: InputDecoration(
                          border: OutlineInputBorder(),
                          labelText: 'Enter Grade(%)',
                          hintText: 'Enter Grade(%)',
                        ),
                      ),
                    ),
                  ),
                ),
                Expanded(
                  child: Padding(
                      padding: const EdgeInsets.all(8.0),
                      child: Text("(Visible only to user)")),
                )
              ],
            ),
            Spacer(),
            Padding(
              padding: const EdgeInsets.all(8.0),
              child: Align(
                alignment: Alignment.bottomCenter,
                child: Column(
                  children: [
                    vGap(20),
                    Container(
                      width: size?.wp(87),
                      height: size?.hp(5),
                      decoration: BoxDecoration(
                          color: secondaryColor,
                          borderRadius: BorderRadius.circular(10)),
                      child: TextButton(
                        onPressed: () {
                          // Access the values using the controllers
                          print(
                              'Higher Education Start Year: $dropdownValueStartYearHigher');
                          print(
                              'Higher Education End Year: $dropdownValueEndYearHigher');
                          print(
                              'Higher Education Grade: ${gradeControllerHigher.text}');

                          print(
                              'Secondary Education Start Year: $dropdownValueStartYearSecondary');
                          print(
                              'Secondary Education End Year: $dropdownValueEndYearSecondary');
                          print(
                              'Secondary Education Grade: ${gradeControllerSecondary.text}');
                          sendDataToBackend();
                        },
                        child: Text(
                          'Submit',
                          textScaleFactor: 1.25,
                          style: TextStyle(
                            color: thirdColor,
                            fontFamily: 'Roboto',
                            fontWeight: FontWeight.w700,
                          ),
                        ),
                      ),
                    ),
                  ],
                ),
              ),
            ),
          ],
        ),
      ),
    );
  }
}
