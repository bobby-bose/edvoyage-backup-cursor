import 'package:flutter/material.dart';
import 'package:webview_flutter/webview_flutter.dart';
import 'package:frontend/utils/colors/colors.dart';

class VideoPlayerScreen extends StatefulWidget {
  final Map<String, dynamic> videoData;

  const VideoPlayerScreen({
    super.key,
    required this.videoData,
  });

  @override
  _VideoPlayerScreenState createState() => _VideoPlayerScreenState();
}

class _VideoPlayerScreenState extends State<VideoPlayerScreen> {
  late WebViewController _webViewController;
  bool _isPlaying = false;
  bool _isCompleted = false;
  bool _showControls = true;
  final Duration _currentPosition = Duration.zero;
  final Duration _totalDuration = Duration(minutes: 30); // Default 30 minutes
  double _progress = 0.0;
  bool _isLoading = true;

  @override
  void initState() {
    super.initState();
    _initializeVideoPlayer();
  }

  void _initializeVideoPlayer() {
    _webViewController = WebViewController()
      ..setJavaScriptMode(JavaScriptMode.unrestricted)
      ..setNavigationDelegate(
        NavigationDelegate(
          onPageStarted: (String url) {
            setState(() {
              _isLoading = true;
            });
          },
          onPageFinished: (String url) {
            setState(() {
              _isLoading = false;
            });
          },
        ),
      )
      ..loadRequest(Uri.parse(_getYouTubeEmbedUrl()));
  }

  String _getYouTubeEmbedUrl() {
    // Extract video ID from YouTube URL
    String videoUrl = widget.videoData['videoUrl'] ?? '';
    String videoId = '';

    if (videoUrl.contains('youtube.com/watch?v=')) {
      videoId = videoUrl.split('v=')[1].split('&')[0];
    } else if (videoUrl.contains('youtu.be/')) {
      videoId = videoUrl.split('youtu.be/')[1].split('?')[0];
    }

    // Return embed URL with autoplay and controls
    return 'https://www.youtube.com/embed/$videoId?autoplay=1&controls=1&rel=0&showinfo=0&modestbranding=1';
  }

  void _togglePlayPause() {
    setState(() {
      _isPlaying = !_isPlaying;
    });
    // JavaScript to control YouTube player
    _webViewController.runJavaScript(
        _isPlaying ? 'player.playVideo();' : 'player.pauseVideo();');
  }

  void _seekBackward() {
    _webViewController
        .runJavaScript('player.seekTo(player.getCurrentTime() - 5);');
  }

  void _seekForward() {
    _webViewController
        .runJavaScript('player.seekTo(player.getCurrentTime() + 5);');
  }

  void _markAsCompleted() async {
    setState(() {
      _isCompleted = true;
    });

    // TODO: API call to mark video as completed
    print('Marking video as completed: ${widget.videoData['title']}');

    // Show success message
    ScaffoldMessenger.of(context).showSnackBar(
      SnackBar(
        content: Text('Video marked as completed!'),
        backgroundColor: Colors.green,
        duration: Duration(seconds: 2),
      ),
    );
  }

  void _openSettings() {
    showModalBottomSheet(
      context: context,
      backgroundColor: Colors.transparent,
      builder: (context) => _buildSettingsSheet(),
    );
  }

  Widget _buildSettingsSheet() {
    return Container(
      decoration: BoxDecoration(
        color: whiteColor,
        borderRadius: BorderRadius.only(
          topLeft: Radius.circular(20),
          topRight: Radius.circular(20),
        ),
      ),
      child: Column(
        mainAxisSize: MainAxisSize.min,
        children: [
          Container(
            margin: EdgeInsets.only(top: 8),
            width: 40,
            height: 4,
            decoration: BoxDecoration(
              color: grey3,
              borderRadius: BorderRadius.circular(2),
            ),
          ),
          Padding(
            padding: EdgeInsets.all(20),
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Text(
                  'Video Settings',
                  style: TextStyle(
                    fontFamily: 'Poppins',
                    fontSize: 18,
                    fontWeight: FontWeight.w600,
                    color: titlecolor,
                  ),
                ),
                SizedBox(height: 20),
                _buildSettingItem('Playback Speed', '1.0x', Icons.speed),
                _buildSettingItem('Quality', 'Auto', Icons.high_quality),
                _buildSettingItem('Subtitles', 'Off', Icons.subtitles),
                _buildSettingItem('Audio Track', 'Default', Icons.audiotrack),
              ],
            ),
          ),
        ],
      ),
    );
  }

  Widget _buildSettingItem(String title, String value, IconData icon) {
    return Padding(
      padding: EdgeInsets.symmetric(vertical: 8),
      child: Row(
        children: [
          Icon(icon, color: grey3, size: 20),
          SizedBox(width: 12),
          Expanded(
            child: Text(
              title,
              style: TextStyle(
                fontFamily: 'Poppins',
                fontSize: 16,
                color: titlecolor,
              ),
            ),
          ),
          Text(
            value,
            style: TextStyle(
              fontFamily: 'Poppins',
              fontSize: 14,
              color: grey3,
            ),
          ),
          SizedBox(width: 8),
          Icon(Icons.chevron_right, color: grey3, size: 16),
        ],
      ),
    );
  }

  Widget _buildVerticalProgressBar() {
    return SizedBox(
      width: 60,
      child: Column(
        children: [
          // Current time
          Text(
            '${_currentPosition.inMinutes}:${(_currentPosition.inSeconds % 60).toString().padLeft(2, '0')}',
            style: TextStyle(
              fontFamily: 'Poppins',
              fontSize: 12,
              color: whiteColor,
            ),
          ),
          SizedBox(height: 8),
          // Progress bar
          Expanded(
            child: RotatedBox(
              quarterTurns: 3,
              child: SliderTheme(
                data: SliderTheme.of(context).copyWith(
                  trackHeight: 4,
                  thumbShape: RoundSliderThumbShape(enabledThumbRadius: 6),
                  overlayShape: RoundSliderOverlayShape(overlayRadius: 12),
                  activeTrackColor: secondaryColor,
                  inactiveTrackColor: grey3.withOpacity(0.3),
                  thumbColor: secondaryColor,
                ),
                child: Slider(
                  value: _progress,
                  onChanged: (value) {
                    setState(() {
                      _progress = value;
                    });
                    // Seek to position
                    int seekTime = (value * _totalDuration.inSeconds).round();
                    _webViewController
                        .runJavaScript('player.seekTo($seekTime);');
                  },
                ),
              ),
            ),
          ),
          SizedBox(height: 8),
          // Total duration
          Text(
            '${_totalDuration.inMinutes}:${(_totalDuration.inSeconds % 60).toString().padLeft(2, '0')}',
            style: TextStyle(
              fontFamily: 'Poppins',
              fontSize: 12,
              color: whiteColor,
            ),
          ),
        ],
      ),
    );
  }

  Widget _buildPlaybackControls() {
    return Container(
      padding: EdgeInsets.symmetric(horizontal: 20, vertical: 10),
      decoration: BoxDecoration(
        color: Colors.black.withOpacity(0.7),
        borderRadius: BorderRadius.circular(25),
      ),
      child: Row(
        mainAxisSize: MainAxisSize.min,
        children: [
          // Rewind 5 seconds
          IconButton(
            onPressed: _seekBackward,
            icon: Icon(Icons.replay_5, color: whiteColor, size: 24),
          ),
          SizedBox(width: 16),
          // Play/Pause
          IconButton(
            onPressed: _togglePlayPause,
            icon: Icon(
              _isPlaying ? Icons.pause : Icons.play_arrow,
              color: whiteColor,
              size: 32,
            ),
          ),
          SizedBox(width: 16),
          // Forward 5 seconds
          IconButton(
            onPressed: _seekForward,
            icon: Icon(Icons.forward_5, color: whiteColor, size: 24),
          ),
        ],
      ),
    );
  }

  Widget _buildBreadcrumbs() {
    return Container(
      padding: EdgeInsets.all(16),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.end,
        children: [
          Icon(Icons.book, color: whiteColor, size: 20),
          SizedBox(height: 8),
          RotatedBox(
            quarterTurns: 3,
            child: Text(
              '📘 / Video / ${widget.videoData['categoryTitle'] ?? 'Unknown'} / ${widget.videoData['title'] ?? 'Unknown'}',
              style: TextStyle(
                fontFamily: 'Poppins',
                fontSize: 12,
                color: whiteColor,
              ),
            ),
          ),
        ],
      ),
    );
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: Colors.black,
      body: SafeArea(
        child: Stack(
          children: [
            // Video Player
            SizedBox(
              width: double.infinity,
              height: double.infinity,
              child: _isLoading
                  ? Center(
                      child: Column(
                        mainAxisAlignment: MainAxisAlignment.center,
                        children: [
                          CircularProgressIndicator(
                            color: secondaryColor,
                            strokeWidth: 3,
                          ),
                          SizedBox(height: 16),
                          Text(
                            'Loading Video...',
                            style: TextStyle(
                              fontFamily: 'Poppins',
                              fontSize: 16,
                              color: whiteColor,
                            ),
                          ),
                        ],
                      ),
                    )
                  : WebViewWidget(controller: _webViewController),
            ),

            // Vertical Progress Bar (Left)
            Positioned(
              left: 20,
              top: 0,
              bottom: 0,
              child: _buildVerticalProgressBar(),
            ),

            // Breadcrumbs (Right)
            Positioned(
              right: 20,
              top: 0,
              bottom: 0,
              child: _buildBreadcrumbs(),
            ),

            // Playback Controls (Center)
            if (_showControls)
              Positioned(
                left: 0,
                right: 0,
                top: 0,
                bottom: 0,
                child: Center(
                  child: _buildPlaybackControls(),
                ),
              ),

            // Bottom Controls
            Positioned(
              bottom: 20,
              left: 20,
              right: 20,
              child: Row(
                mainAxisAlignment: MainAxisAlignment.spaceBetween,
                children: [
                  // Settings Button
                  GestureDetector(
                    onTap: _openSettings,
                    child: Container(
                      padding: EdgeInsets.all(12),
                      decoration: BoxDecoration(
                        color: Colors.black.withOpacity(0.7),
                        borderRadius: BorderRadius.circular(8),
                      ),
                      child: Icon(
                        Icons.settings,
                        color: whiteColor,
                        size: 24,
                      ),
                    ),
                  ),

                  // Mark Completed Button
                  if (!_isCompleted)
                    GestureDetector(
                      onTap: _markAsCompleted,
                      child: Container(
                        padding:
                            EdgeInsets.symmetric(horizontal: 16, vertical: 8),
                        decoration: BoxDecoration(
                          color: Colors.green,
                          borderRadius: BorderRadius.circular(20),
                          border: Border.all(color: Colors.green, width: 2),
                        ),
                        child: Text(
                          'Mark Completed',
                          style: TextStyle(
                            fontFamily: 'Poppins',
                            fontSize: 14,
                            fontWeight: FontWeight.w600,
                            color: whiteColor,
                          ),
                        ),
                      ),
                    )
                  else
                    Container(
                      padding:
                          EdgeInsets.symmetric(horizontal: 16, vertical: 8),
                      decoration: BoxDecoration(
                        color: Colors.grey.withOpacity(0.3),
                        borderRadius: BorderRadius.circular(20),
                      ),
                      child: Row(
                        mainAxisSize: MainAxisSize.min,
                        children: [
                          Icon(Icons.check, color: whiteColor, size: 16),
                          SizedBox(width: 4),
                          Text(
                            'Completed',
                            style: TextStyle(
                              fontFamily: 'Poppins',
                              fontSize: 14,
                              fontWeight: FontWeight.w600,
                              color: whiteColor,
                            ),
                          ),
                        ],
                      ),
                    ),
                ],
              ),
            ),

            // Tap to show/hide controls
            Positioned.fill(
              child: GestureDetector(
                onTap: () {
                  setState(() {
                    _showControls = !_showControls;
                  });
                },
                child: Container(
                  color: Colors.transparent,
                ),
              ),
            ),
          ],
        ),
      ),
    );
  }
}
