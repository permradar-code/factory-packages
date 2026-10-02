import json, copy
base = json.load(open('../c130v2/input.json'))
SCRIPT = """This pilot just ejected. His jet didn't.

February 1970. Montana. Lieutenant Gary Foust is in a training dogfight in an F-106 Delta Dart, when his jet falls into a flat spin. Nothing he does can stop it. At fifteen thousand feet, he pulls the handle and ejects.

Then something strange happens. Without the pilot, the jet's balance changes. The nose drops, the spin stops, and the empty jet levels out and keeps flying.

Hanging under his parachute, Foust hears another pilot on the radio: "Gary, you'd better get back in it!"

Nobody is at the controls. The jet glides lower and lower over the snow, and settles onto its belly in a farmer's field. Almost gently.

The engine is still running. The local sheriff arrives and calls the air base for instructions. When he climbs up to the cockpit, the jet starts sliding forward on the snow. So he climbs back down and waits for it to run out of fuel.

The damage is so minor that the Air Force takes off the wings, ships it out by train, repairs it, and sends it back into service. Pilots call it the Cornfield Bomber.

Nine years later, Gary Foust climbs into that same jet again. He finally got back in it.

Today it sits in the National Museum of the United States Air Force. Some landings aren't in the manual."""

JET = ("the grey F-106 Delta Dart (tailless delta wing with NO horizontal stabilizers, tall vertical fin with a "
       "squared-off flat top, slim area-ruled fuselage, intakes on both sides behind the cockpit)")
LOOK = "1970 color film look, realistic, no text, no readable markings"

def img(i, cue, prompt, dur=3.5, refs=("F106",)):
    return {"id": i, "type": "image", "duration_s": dur, "narration_cue": cue, "references": list(refs),
            "image_prompt_full": f"Photorealistic vertical shot. {prompt} {LOOK}.", "motion_prompt": None}

shots = [
 {"id": "001", "type": "video", "duration_s": 6.0, "narration_cue": "This pilot just ejected", "references": ["F106"],
  "image_prompt_full": f"Photorealistic vertical shot, high above snowy Montana plains on a clear frigid day. In the upper foreground a USAF pilot in a 1970 flight suit and white helmet hangs under an orange-and-white round parachute, seen from behind and slightly above, looking down. Far below him {JET} flies straight and level on its own, canopy gone, small against the white snow. {LOOK}.",
  "end_image_prompt_full": f"Same scene and lighting a few seconds later: the pilot under the parachute in the same place in the upper foreground, while {JET} below has flown further away toward the right edge of the frame, smaller, still level, its shadow on the snow. {LOOK}.",
  "motion_prompt": "The pilot swings gently under the parachute while far below the empty jet keeps flying straight and level, moving away across the snowy plains. Slow, eerie, calm. No fire, no explosion."},
 img("002", "February 1970", f"Two {JET.replace('the grey', 'grey')} flying high over snow-covered Montana mountains under a deep blue sky, vapor trails curling as they turn toward each other."),
 img("003", "training dogfight", f"{JET} in a hard climbing turn, condensation streaming off the delta wing tips, seen from a chase plane, bright winter sky."),
 img("004", "flat spin", f"{JET} spinning flat like a falling leaf, nose level, rotating, seen from above with the snowy ground far below and the horizon tilted."),
 img("005", "Nothing he does", "Inside a 1970 jet fighter cockpit: a pilot's gloved hands gripping the control stick, red warning lights on a grey analog instrument panel, the snowy ground and horizon blurred and rotating outside the canopy. Tense."),
 img("006", "pulls the handle", f"{JET} seen from outside: the canopy has blown off and the ejection seat with the pilot is rising out of the cockpit on a short rocket plume, snowy land far below."),
 img("007", "something strange happens", f"Close view of {JET} from above and behind: the open cockpit is completely empty, no canopy and no seat, while the jet flies on by itself over the snow."),
 img("008", "The nose drops", f"{JET} with an empty open cockpit recovering from the spin, nose pitched down, wings leveling, snowy plains below, seen from a chase plane."),
 img("009", "Hanging under his parachute", "A USAF pilot in a 1970 white helmet and olive flight suit hanging under a round orange-and-white parachute, close up from the side, looking down in disbelief, snowy mountains below, clear cold sky.", refs=()),
 img("010", "you'd better get back in it", f"View from the cockpit of a second fighter flying in formation: alongside, {JET} flies level with its cockpit completely empty and open, nobody inside, snowy plains below."),
 {"id": "011", "type": "video", "duration_s": 8.0, "narration_cue": "Nobody is at the controls", "references": ["F106"],
  "image_prompt_full": f"Photorealistic vertical low side view: {JET}, with an empty open cockpit and landing gear UP, gliding a few meters above a flat snow-covered farm field toward the camera, fence posts and a distant farmhouse, overcast winter light. {LOOK}.",
  "end_image_prompt_full": f"Same field and lighting: {JET} now resting on its belly in the snow in the middle of the field, gear up, intact, empty open cockpit, a long furrow behind it and a cloud of snow powder settling. {LOOK}.",
  "motion_prompt": "The empty jet glides lower and lower, touches the snow on its belly and slides to a smooth stop, throwing up a soft cloud of powder snow. Gentle, no crash, no fire, no explosion, no smoke."},
 img("012", "The engine is still running", f"{JET} sitting on its belly in a snowy farm field, empty open cockpit, heat shimmer and faint exhaust vapor behind the tail, cold blue afternoon light."),
 img("013", "The local sheriff arrives", f"A 1970 Montana county sheriff in a cowboy hat and sheepskin coat walking through deep snow toward {JET} resting on its belly in a field, his old sheriff's car parked by the road behind him.", ),
 img("014", "When he climbs up to the cockpit", f"The sheriff in a cowboy hat clinging to the side of {JET} next to the open cockpit as the jet creeps forward on the snow, startled expression, snow spraying under the belly."),
 img("015", "waits for it to run out of fuel", f"The sheriff and two local farmers in winter coats standing at a distance in the snow, arms folded, watching {JET} sitting in the field, exhaust vapor behind it, late afternoon light."),
 img("016", "takes off the wings", f"The fuselage of {JET} with its wings removed, strapped onto a railroad flatcar on a train crossing a snowy Montana landscape."),
 img("017", "Cornfield Bomber", f"{JET}, repaired and polished, parked on a sunny air force flight line with ground crew in 1970s uniforms walking around it."),
 img("018", "Nine years later", f"A USAF pilot in his late thirties with a mustache, in a 1979 flight suit, climbing the boarding ladder into the cockpit of {JET} on a sunny Florida flight line, smiling slightly."),
 img("019", "Today it sits", f"{JET} on display inside a large modern aviation museum hall, visitors looking up at it, soft museum lighting."),
 img("020", "Some landings aren't in the manual", f"Cinematic silhouette of {JET} flying alone low over endless snowy plains at sunset, orange sky, the cockpit empty. Epic and quiet."),
]

d = copy.deepcopy(base)
d.update({"project_id": "nitm_f106_cornfield_v1", "title": "He Ejected. His Jet Didn't.", "script": SCRIPT, "shots": shots,
          "references": {"F106": {"type": "aircraft", "prompt_raw": True, "views": ["three_quarter"],
            "description": "Photorealistic reference of a 1970 USAF Convair F-106A Delta Dart interceptor. Single-engine supersonic jet. TAILLESS DELTA WING: a large triangular wing and NO horizontal stabilizers at all. One tall vertical fin with a distinctive SQUARED-OFF FLAT TOP (not pointed). Slim area-ruled 'coke bottle' fuselage, pointed nose, bubble canopy, air intakes on both sides of the fuselage just behind the cockpit, single exhaust at the rear. Overall light Air Defense Command grey paint, small USAF star-and-bar insignia, no readable text. Clean three-quarter front view on a plain light grey background, no watermark."}},
          "music": {"prompt": "Tense, eerie cinematic documentary score: slow pulsing low strings, sparse piano notes, cold airy pads, building quietly toward a warm hopeful resolve. No vocals, no drums kit.",
                    "model": "lyria-3-pro-preview", "duration_s": 90, "instrumental": True},
          "delivery": {"github": {"repo": "permradar-code/factory-packages"}}})
json.dump(d, open('input_f106_v1.json', 'w'), ensure_ascii=False, indent=1)
print(len(SCRIPT.split()), 'words;', len(shots), 'shots')
