from read_parse_toktab import process_similar, capitalize_all


def test_process_similar():
    pairs = [
        ('458', '"!ad","d"+$80,"I",-2', ('458+4 TkAd2:\tdc.w CAdd2-Tk,Synt-Tk', '+6 \tdc.b "!ad","d"+$80,"I",-2')),
        ('462', '$80,"I",-1', ('462+4 TkAd4:\tdc.w CAdd4-Tk,Synt-Tk', '+4 \tdc.b $80,"I",-1'))
    ]
    out = list(process_similar(pairs))
    assert(out[1][1] == '"ad","d"+$80,"I",-2')


def test_capitalize_all():
    """It should capitalize all the words in the line"""
    line = "the quick brown fox"
    assert(capitalize_all(line) == "The Quick Brown Fox")

# def test_get_tokens_from_lines():
#     """Test that given a sample set of toktab lines,
#         the tokens can be read from them sensibly"""
#     sample = """
#     FFFFFF98+4 	dc.w CSupEg-Tk,Synt-Tk
#         +6 	dc.b "=",">"+$80,"O20",-1
#     3C0+4 	dc.w 0,L_Stop
#         +6 	dc.b "sto","p"+$80,"I",-1
#     46A+4 TkHPr:	dc.w CHPrnt-Tk,Synt-Tk
#         +8 	dc.b "print ","#"+$80,-1
#     476+4 TkPr:	dc.w CPrnt-Tk,Synt-Tk
#         +8 	dc.b "prin","t"+$80,"I",-1
#     """.splitlines()
#