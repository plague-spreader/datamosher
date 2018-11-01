ffprobe -show_frames -select_streams v:0 corsa.mpg 2>/dev/null | grep -E "(pkt_pos|pkt_size|pict_type)"
