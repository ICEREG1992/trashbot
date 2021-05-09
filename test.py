import karaoke

a = karaoke.word_set(karaoke.Karaoke.format("i've been feeling underconfident underneath my skin").split(" "))
b = karaoke.word_set(karaoke.Karaoke.format("so can feeling underconfident").split(" "))

print(karaoke.Karaoke.comes_first(a, b))
karaoke.Karaoke.align_sets(a, b)
print(str(a) + " // " + str(b))