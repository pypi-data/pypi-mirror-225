from regular_regexes.regular_regexes import rre

def test_email():
    assert len(rre.email("test@test.com")) > 0
    assert len(rre.email("test@test")) == 0

def test_url():
    assert len(rre.url("check it at test.com")) > 0
    assert len(rre.url("check it at testcom")) == 0
    assert len(rre.url("check it at https://test.com")) > 0
    assert len(rre.url("check it at https://testcom")) == 0

def test_multiple_punctuation():
    assert len(rre.multiple_punctuation("how are you??")) > 0
    assert len(rre.multiple_punctuation("how are you?!")) > 0
    assert len(rre.multiple_punctuation("&&&&& that's how it is")) > 0
    assert len(rre.multiple_punctuation("& that's how it is")) == 0
    assert len(rre.multiple_punctuation("how are you?")) == 0
    assert len(rre.multiple_punctuation("look over there!")) == 0