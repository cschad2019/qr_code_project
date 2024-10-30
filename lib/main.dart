import 'package:flutter/material.dart';

void main() => runApp(StyleQRApp());

class StyleQRApp extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Style QR',
      theme: ThemeData(
        primarySwatch: Colors.blue,
        brightness: Brightness.light,
      ),
      home: QRHomePage(),
    );
  }
}

class QRHomePage extends StatefulWidget {
  @override
  _QRHomePageState createState() => _QRHomePageState();
}

class _QRHomePageState extends State<QRHomePage> {
  String? inputUrl; // Store the URL input by the user
  final TextEditingController urlController = TextEditingController(); // Controller for the TextField

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text('Style QR'),
        centerTitle: true,
        backgroundColor: Colors.blueAccent,
      ),
      body: Padding(
        padding: const EdgeInsets.all(16.0),
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            Text(
              'Generate a Custom QR Code',
              style: TextStyle(
                fontSize: 24,
                fontWeight: FontWeight.bold,
                color: Colors.blueAccent,
              ),
              textAlign: TextAlign.center,
            ),
            SizedBox(height: 20),
            TextField(
              controller: urlController, // Link the controller to the TextField
              decoration: InputDecoration(
                labelText: 'Enter Website URL',
                border: OutlineInputBorder(),
                filled: true,
                fillColor: Colors.blue.shade50,
              ),
              onChanged: (value) {
                setState(() {
                  inputUrl = value; // Update inputUrl whenever the text changes
                });
              },
            ),
            SizedBox(height: 20),
            ElevatedButton(
              onPressed: () {
                if (inputUrl != null && inputUrl!.isNotEmpty) {
                  print('Generate QR Code for $inputUrl');
                } else {
                  ScaffoldMessenger.of(context).showSnackBar(
                    SnackBar(content: Text('Please enter a URL')),
                  );
                }
              },
              child: Text('Generate QR Code'),
              style: ElevatedButton.styleFrom(
                padding: EdgeInsets.symmetric(horizontal: 30, vertical: 15),
              ),
            ),
          ],
        ),
      ),
    );
  }
}
