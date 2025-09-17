import 'dart:convert';
import 'package:flutter/material.dart';
import 'package:flutter/services.dart';
import 'package:http/http.dart' as http;
import 'package:intl/intl.dart';
import 'package:frontend/_env/env.dart';
import 'package:frontend/utils/colors/colors.dart';

class MCQQuestionWidget extends StatefulWidget {
  const MCQQuestionWidget({super.key});

  @override
  _MCQQuestionWidgetState createState() => _MCQQuestionWidgetState();
}

class _MCQQuestionWidgetState extends State<MCQQuestionWidget> {
  List<Map<String, dynamic>> questions = [];
  bool isLoading = true;

  // Sample MCQ questions as fallback
  final List<Map<String, dynamic>> sampleQuestions = [
    {
      'question':
          'Which of the following is the largest organ in the human body?',
      'options': ['Heart', 'Liver', 'Skin', 'Brain'],
      'correct_answer': 2,
      'explanation':
          'The skin is the largest organ in the human body, covering approximately 20 square feet in adults.',
    },
    {
      'question': 'What is the normal range for blood pressure in adults?',
      'options': ['90/60 mmHg', '120/80 mmHg', '140/90 mmHg', '160/100 mmHg'],
      'correct_answer': 1,
      'explanation':
          'Normal blood pressure is typically around 120/80 mmHg, with systolic pressure of 120 and diastolic pressure of 80.',
    },
  ];

  @override
  void initState() {
    super.initState();
    loadDailyQuestions();
  }

  Future<void> loadDailyQuestions() async {
    try {
      // First try to fetch from API
      final today = DateFormat('yyyy-MM-dd').format(DateTime.now());
      final response = await http.get(
        Uri.parse('${BaseUrl.mcqQuestionOfTheDay}?date=$today'),
      );

      if (response.statusCode == 200) {
        final data = jsonDecode(response.body);
        if (data is List && data.isNotEmpty) {
          setState(() {
            questions = data
                .map((questionData) => {
                      'question':
                          questionData['question_text'] ?? 'No QUESTION',
                      'options': (questionData['options'] as List?)
                              ?.map((e) =>
                                  e['option_text']?.toString() ?? 'NO OPTION')
                              .toList() ??
                          ['NO OPTION'],
                      'correct_answer': questionData['correct_answer'] ?? 0,
                      'explanation': questionData['explanation'] ?? '',
                      'selected_option': null,
                      'show_answer': false,
                    })
                .toList();
            isLoading = false;
          });
          return;
        }
      }
    } catch (e) {
      print('API Error: $e');
    }

    // If API fails, load from JSON file
    await loadFromJsonFile();
  }

  Future<void> loadFromJsonFile() async {
    try {
      // Get current day of month (1-31)
      // This ensures questions change daily and repeat monthly
      final currentDay = DateTime.now().day.toString();
      print('Loading questions for day: $currentDay'); // Debug log

      // Load JSON file
      final jsonString =
          await rootBundle.loadString('assets/daily_mcq_questions.json');
      final jsonData = jsonDecode(jsonString);

      final dailyQuestions = jsonData['daily_questions'];
      print(
          'Available days in JSON: ${dailyQuestions.keys.toList()}'); // Debug log

      if (dailyQuestions != null && dailyQuestions[currentDay] != null) {
        final dayQuestions = dailyQuestions[currentDay] as List;
        print(
            'Found ${dayQuestions.length} questions for day $currentDay'); // Debug log

        if (dayQuestions.isNotEmpty) {
          setState(() {
            questions = dayQuestions
                .map((questionData) => {
                      'question':
                          questionData['question'] ?? 'No question available',
                      'options':
                          List<String>.from(questionData['options'] ?? []),
                      'correct_answer': questionData['correct_answer'] ?? 0,
                      'explanation': questionData['explanation'] ?? '',
                      'selected_option': null,
                      'show_answer': false,
                    })
                .toList();
            isLoading = false;
          });
          return;
        }
      } else {
        print(
            'No questions found for day $currentDay, using fallback'); // Debug log
      }
    } catch (e) {
      print('JSON Error: $e');
    }

    // Use sample questions as fallback
    setState(() {
      questions = sampleQuestions
          .map((questionData) => {
                'question': questionData['question'],
                'options': List<String>.from(questionData['options']),
                'correct_answer': questionData['correct_answer'],
                'explanation': questionData['explanation'],
                'selected_option': null,
                'show_answer': false,
              })
          .toList();
      isLoading = false;
    });
  }

  void _selectOption(int questionIndex, int optionIndex) {
    setState(() {
      questions[questionIndex]['selected_option'] = optionIndex;
      questions[questionIndex]['show_answer'] = true;
    });
  }

  @override
  Widget build(BuildContext context) {
    if (isLoading) {
      return Card(
        margin: EdgeInsets.symmetric(vertical: 10, horizontal: 10),
        child: Padding(
          padding: const EdgeInsets.all(16.0),
          child: Center(child: CircularProgressIndicator()),
        ),
      );
    }

    return Column(
      children: questions.asMap().entries.map((entry) {
        final questionIndex = entry.key;
        final questionData = entry.value;
        final question = questionData['question'] as String;
        final options = questionData['options'] as List<String>;
        final correctAnswer = questionData['correct_answer'] as int;
        final explanation = questionData['explanation'] as String;
        final selectedOption = questionData['selected_option'] as int?;
        final showAnswer = questionData['show_answer'] as bool;

        return Card(
          margin: EdgeInsets.symmetric(vertical: 8, horizontal: 10),
          elevation: 4,
          child: Padding(
            padding: const EdgeInsets.all(16.0),
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Row(
                  children: [
                    Icon(Icons.quiz, color: primaryColor, size: 20),
                    SizedBox(width: 8),
                    Text(
                      'Question ${questionIndex + 1}',
                      style: TextStyle(
                        fontWeight: FontWeight.bold,
                        color: primaryColor,
                        fontSize: 16,
                      ),
                    ),
                    Spacer(),
                    Container(
                      padding: EdgeInsets.symmetric(horizontal: 8, vertical: 4),
                      decoration: BoxDecoration(
                        color: primaryColor.withValues(alpha: 0.1),
                        borderRadius: BorderRadius.circular(12),
                        border: Border.all(
                            color: primaryColor.withValues(alpha: 0.3)),
                      ),
                      child: Text(
                        'Day ${DateTime.now().day}',
                        style: TextStyle(
                          color: primaryColor,
                          fontSize: 12,
                          fontWeight: FontWeight.bold,
                        ),
                      ),
                    ),
                  ],
                ),
                SizedBox(height: 12),
                Text(
                  question,
                  style: TextStyle(
                    fontWeight: FontWeight.bold,
                    fontSize: 16,
                    color: fourthColor,
                  ),
                ),
                SizedBox(height: 16),
                ...options.asMap().entries.map((optionEntry) {
                  final index = optionEntry.key;
                  final option = optionEntry.value;
                  final isSelected = selectedOption == index;
                  final isCorrect = index == correctAnswer;

                  return Padding(
                    padding: const EdgeInsets.symmetric(vertical: 4.0),
                    child: InkWell(
                      onTap: () => _selectOption(questionIndex, index),
                      child: Container(
                        padding: EdgeInsets.all(12),
                        decoration: BoxDecoration(
                          border: Border.all(
                            color: isSelected
                                ? (isCorrect
                                    ? ColorConst.greenColor
                                    : ColorConst.errorColor)
                                : grey1,
                            width: 2,
                          ),
                          borderRadius: BorderRadius.circular(8),
                          color: isSelected
                              ? (isCorrect
                                  ? ColorConst.greenColor.withValues(alpha: 0.1)
                                  : ColorConst.errorColor
                                      .withValues(alpha: 0.1))
                              : thirdColor,
                        ),
                        child: Row(
                          children: [
                            Container(
                              width: 20,
                              height: 20,
                              decoration: BoxDecoration(
                                shape: BoxShape.circle,
                                color: isSelected
                                    ? (isCorrect
                                        ? ColorConst.greenColor
                                        : ColorConst.errorColor)
                                    : grey1,
                              ),
                              child: Center(
                                child: isSelected
                                    ? Icon(
                                        isCorrect ? Icons.check : Icons.close,
                                        color: thirdColor,
                                        size: 14,
                                      )
                                    : Text(
                                        String.fromCharCode(
                                            65 + index), // A, B, C, D
                                        style: TextStyle(
                                          color: grey3,
                                          fontWeight: FontWeight.bold,
                                        ),
                                      ),
                              ),
                            ),
                            SizedBox(width: 12),
                            Expanded(
                              child: Text(
                                option,
                                style: TextStyle(
                                  fontSize: 14,
                                  color: isSelected
                                      ? (isCorrect
                                          ? ColorConst.greenColor
                                          : ColorConst.errorColor)
                                      : fourthColor,
                                ),
                              ),
                            ),
                          ],
                        ),
                      ),
                    ),
                  );
                }),
                if (showAnswer) ...[
                  SizedBox(height: 12),
                  Container(
                    padding: EdgeInsets.all(8),
                    decoration: BoxDecoration(
                      color: primaryColor.withValues(alpha: 0.1),
                      borderRadius: BorderRadius.circular(8),
                      border: Border.all(
                          color: primaryColor.withValues(alpha: 0.3)),
                    ),
                    child: Column(
                      crossAxisAlignment: CrossAxisAlignment.start,
                      children: [
                        Row(
                          children: [
                            Icon(Icons.lightbulb,
                                color: primaryColor, size: 16),
                            SizedBox(width: 8),
                            Text(
                              'Correct answer: ${options[correctAnswer]}',
                              style: TextStyle(
                                color: primaryColor,
                                fontWeight: FontWeight.w500,
                              ),
                            ),
                          ],
                        ),
                        if (explanation.isNotEmpty) ...[
                          SizedBox(height: 8),
                          Text(
                            explanation,
                            style: TextStyle(
                              color: primaryColor.withValues(alpha: 0.8),
                              fontSize: 12,
                            ),
                          ),
                        ],
                      ],
                    ),
                  ),
                ],
              ],
            ),
          ),
        );
      }).toList(),
    );
  }
}
