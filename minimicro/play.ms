// Demo of HALO effect in Mini Micro (https://miniscript.org/MiniMicro).
// Because the Mini Micro API does not provide easy access to the raw
// waveform of sounds loaded from files, we opt for a simpler approach:
// load the sound twice, and play the second copy after a 20-ms delay.

import "stringUtil"

path = "../preset_speech/af_heart_01.wav"

playClip = function(path, withHalo=true)
	snd = file.loadSound(path)
	if snd == null then
		print "Unable to load sound file:"
		print path
		exit
	end if
	if not withHalo then
		snd.play
	else
		snd2 = file.loadSound(path)		
		snd.play; wait 0.02; snd2.play
	end if
end function

voices = [
  ["af_heart",  "American female"],
  ["am_adam",   "American male"],
  ["bf_emma",   "British female"],
  ["bm_george", "British male"]]

presets = [
  "HALO is an audible effect that makes synthetic speech easily identifiable, yet still clear.",
  "You can apply HALO to real-time synthetic speech, or prerendered audio clips.",
  "Consider using HALO whenever you are rendering AI-generated speech."]

getChoice = function(prompt, minVal, maxVal, default=1)
	while true
		inp = input(prompt + " [" + default + "]: ").trim.lower
		if inp == "" then return default
		if inp and inp[0] == "q" then return "q"
		choice = inp.val
		if minVal <= choice <= maxVal then return choice
		print "Please enter a number from {minVal} to {maxVal}, or Q.".fill(locals)
	end while
end function

doOneMenu = function
	print "Voices:"
	for i in range(1, voices.len)
		v = voices[i - 1]
		print "  " + i + ". " + v[1] + "  (" + v[0] + ")"
	end for
	print "  Q. quit"
	print
	voiceNum = getChoice("Voice", 1, voices.len)
	if voiceNum == "q" then exit
	
	print
	for i in range(1, presets.len)
		print "  " + i + ". " + presets[i-1]	
	end for
	sampleNum = getChoice("Preset", 1, presets.len)
	if sampleNum == "q" then exit
	
	print
	doHalo = not input("Apply HALO effect [Y/n]: ").trim.lower.startsWith("n")
	
	clip = voices[voiceNum-1][0] + "_0" + sampleNum + ".wav"
	playClip "../preset_speech/" + clip, doHalo	
	print
end function

while true
	doOneMenu
end while
