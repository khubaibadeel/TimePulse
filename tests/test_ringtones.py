import TimePulse


def validate(filename):
    return TimePulse.AlarmApp.validate_ringtone_filename(
        None,
        filename,
        require_exists=False,
    )


def test_accepts_plain_wav_filename():
    assert validate("Soft_Arrival.wav") == "Soft_Arrival.wav"
    assert validate("tone.WAV") == "tone.WAV"


def test_rejects_paths_and_non_wav_files():
    assert validate("../secret.wav") is None
    assert validate(r"C:\\music\\tone.wav") is None
    assert validate("folder/tone.wav") is None
    assert validate("tone.mp3") is None
    assert validate("") is None


def test_friendly_ringtone_name():
    result = TimePulse.AlarmApp.get_friendly_name(None, "Bell_for_Seven_AM.wav")
    assert result == "Bell for Seven AM"
