from collections import Counter
import string
from typing import List, Tuple


CIPHERTEXT = """Vthq gvr pvwwxgj nc Tsaviwx'p oxpl aindjqw xgwn ustf t gvr hxuqvitsuqtavw, xg rqxhq anwq wqv ustxgwvyw tgo wqv hxuqviwvyw vbdxktsvgwp tivhqtgjvo xg ivjtio wn ngv tgnwqvi. Wqviv tiv tp ztgf nc wqvpv tsuqtavwptp wqviv tiv unpxwxngp nc qxp oxpl, tgo wqxp zdswxusxhxwf zvtgp wqtw Tsaviwxqviv ovkxpvo wqv cxipw unsftsuqtavwxh hxuqvi.Wqxp thqxvkvzvgw—hixwxhts xg wqv qxpwnif nc hifuwnsnjf —Tsaviwx wqvgtonigvo af tgnwqvi ivztiltasv xgkvgwxng: vghxuqvivo hnov.
Xw rtp cniwqxp wqtw qv qto udw gdzavip xg wqv ndwvi ixgj. Xg t wtasv qv uvizdwvowqv gdzavip
1 wn 4 xg wrn-, wqivv-, tgo cndi-oxjxw jindup, cinz 11 wn4444, tgo dpvo wqvpv tp 336 hnovjindup
cni t pztss hnov. "Xg wqxp wtasv,thhnioxgj wn tjivvzvgw, rv pqtss vgwvi xg wqv ktixndp sxgvp tw
wqvgdzavip rqtwvkvi hnzusvwv uqitpvp rv usvtpv, cni vytzusv,hniivpungoxgj wn 12, 'Rv qtkv ztov
ivtof wqv pqxup rqxhq rv uinzxpvotgo pduusxvo wqvz rxwq winnup tgo jitxg.' " Wqvpv hnov ktsdvp
oxo gnwhqtgjv, tgf zniv wqtg wqv zxyvo tsuqtavw nc wqv oxpl oxo. Adw wqv oxjxwpivpdswxgj
cinz tg vghnoxgj rviv wqvg vghxuqvivo rxwq wqv oxpl edpw tp xcwqvf rviv ustxgwvyw svwwvip.
Xg Tsaviwx'p rniop, "Wqvpv gdzavip X wqvgxgpviw xg zf zvpptjv thhnioxgj wn wqv cnizdst nc wqv
hxuqvi, ivuivpvgwxgjwqvz af wqv svwwvip wqtw ovgnwv wqvpv gdzavip." Wqvpv gdzavip
wqdphqtgjvo wqvxi hxuqviwvyw vbdxktsvgwp tp wqv oxpl wdigvo. Qvghv 341,uviqtup zvtgxgj
"Unuv," zxjqw avhnzv ziu tw ngv unpxwxng tgo chn twtgnwqvi. Wqxp hngpwxwdwvp tg vyhvssvgw
cniz nc vghxuqvivo hnov, tgo edpwqnr uivhnhxndp Tsaviwx rtp ztf av pvvg af wqv cthw wqtw wqv
zteniunrvip nc wqv vtiwq oxo gnw avjxg wn vghxuqvi wqvxi hnov zvpptjvp dgwxs400 fvtip stwvi,
gvtw wqv vgo nc wqv 19wq hvgwdif, tgo vkvg wqvg wqvxipfpwvzp rviv zdhq pxzusvi wqtg
wqxp.Tsaviwx'p wqivv ivztiltasv cxipwp—wqv vtisxvpw Rvpwvig vyunpxwxng nchifuwtgtsfpxp,
wqv xgkvgwxng nc unsftsuqtavwxv pdapwxwdwxng, tgo wqvxgkvgwxng nc vghxuqvivo hnov—ztlv
qxz wqv Ctwqvi nc RvpwvigHifuwnsnjf. Adw tswqndjq qxp wivtwxpv rtp udasxpqvo xg Xwtsxtg xg
thnssvhwxng nc qxp rnilp xg 1568, tgo tswqndjq qxp xovtp rviv tapniavo afututs hifuwnsnjxpwp tgo
uviqtup xgcsdvghvo wqv phxvghv'p ovkvsnuzvgw,wqvf gvkvi qto wqv ofgtzxh xzuthw wqtw pdhq
uinoxjxndpthhnzusxpqzvgwp ndjqw wn qtkv uinodhvo. Pfzngop' vktsdtwxng nc qxprnil xg jvgvits
ztf anwq vyustxg rqf tgo pdzztixmv wqv znovig kxvr nc qxp hifuwnsnjxhts hngwixadwxngp:"Wqxp
ztg nc ztgf-pxovo jvgxdp htzv xgwn wqv rniso wnn pnng cni wqvuvicvhw vyvihxpv nc qxp pxgjdsti
cthdswxvp. Rqvwqvi rv ivjtio qxz cinz wqvunxgw nc kxvr nc tiw, nc phxvghv, ni nc sxwvitwdiv, qv
nhhduxvp xg vthqovutiwzvgw wqv unpxwxng nc uivhdipni, uxngvvi, tgo xgoxhtwni. Tsrtfpnixjxgts
tgo tsrtfp cviwxsv, qv uinuqvpxvo nc stgop qv rtp gnw uixkxsvjvown vgwvi, svtkxgj wqv zvznif nc
dim tgo ktixvo jivtwgvpp itwqvi wqtg tgfpnsxo zngdzvgw avqxgo qxz."Unsftsuqtavwxhxwf wnnl
tgnwqvi pwvu cnirtio xg 1518, rxwq wqvtuuvtitghv nc wqv cxipw uixgwvo annl ng hifuwnsnjf,
rixwwvg af ngv nc wqvznpw ctzndp xgwvssvhwdtsp nc qxp otf. Wqxp rtp Enqtggvp Wixwqvzxdp,
tAvgvoxhwxgv zngl rqnpv otaasxgj xg tshqvzf tgo nwqvi zfpwxh unrvipztov qxz ngv nc wqv znpw
ivkvivo cxjdivp xg nhhdsw phxvghv, rqxsv qxpzniv pnsxo phqnstipqxu rng qxz wqv wxwsv nc
"Ctwqvi nc Axaxsxnjituqf." Xg1518, t fvti tgo t qtsc tcwvi qxp ovtwq, qxp Unsfjituqxtv sxaix pvy,
sntggxpWixwqvzxdp taatwxp Uvtunsxwtgx, bdngotz Putgqvxzvgpxp, to ZtyxzxsxtgdzHtvptivz ("Pxy
Annlp nc Unsfjituqf, af Enqtggvp Wixwqvzxdp, Taanw twRdimadij, cnizvisf tw Putgqvxz, cni wqv
Vzuvini Ztyxzxsxtg") rtpudasxpqvo. Af cti wqv adsl nc wqv knsdzv hngpxpwp nc wqv hnsdzgp
ncrniop uixgwvo xg stijv Jnwqxh wfuv wqtw Wixwqvzxdp dpvo xg qxp pfpwvzp nchifuwnjituqf.
Adw xg wqv rnil'p Annl K tuuvtip, cni wqv cxipw wxzv, wqvpbdtiv wtasv, ni wtasvtd. Wqxp xp wqv
tsvzvgwts cniz nc unsftsuqtavwxhpdapwxwdwxng, cni xw vyqxaxwp tss tw nghv tss wqv hxuqvi
tsuqtavwp xg tutiwxhdsti pfpwvz. Wqvpv tiv dpdtssf tss wqv ptzv pvbdvghv nc svwwvip,
adwpqxcwvo wn oxccvivgw unpxwxngp xg ivstwxng wn wqv ustxgwvyw tsuqtavw, tp xgTsaviwx'p
oxpl wqv xggvi tsuqtavw tppdzvo oxccvivgw unpxwxngp xg ivjtio wnwqv ndwvi tsuqtavw. Wqv
ttasvtd pvwp wqvz ndw xg niovisf ctpqxng—wqvtsuqtavwp nc wqv pdhhvppxkv unpxwxngp stxo
ndw xg inrp ngv avsnr wqvnwqvi, vthq tsuqtavw pqxcwvo ngv usthv wn wqv svcw nc wqv ngv tankv.
Vthqinr wqdp nccvip t oxccvivgw pvw nc hxuqvi pdapwxwdwvp wn wqv svwwvip nc
wqv ustxgwvyw tsuqtavw tw wqv wnu. Pxghv wqviv htg av ngsf tp ztgf inrp tpwqviv tiv svwwvip xg
wqv tsuqtavw, wqv wtasvtd xp pbdtiv."""

CIPHER_ALPHABET = string.ascii_lowercase
PLAIN_ALPHABET = "bqfujyncrgvkzodshwlapetixm"
SUBSTITUTION = dict(zip(CIPHER_ALPHABET, PLAIN_ALPHABET))


def letter_frequencies(text: str) -> List[Tuple[str, int, float]]:
	letters = [char.lower() for char in text if char.isalpha() and char.isascii()]
	counts = Counter(letters)
	total = len(letters)
	return [
		(letter, count, count / total * 100)
		for letter, count in counts.most_common()
	]


def decrypt(text: str) -> str:
	result = []
	for char in text:
		plain = SUBSTITUTION.get(char.lower())
		if plain is None:
			result.append(char)
		elif char.isupper():
			result.append(plain.upper())
		else:
			result.append(plain)
	return "".join(result)


def main() -> None:
	if len(PLAIN_ALPHABET) != 26 or len(set(PLAIN_ALPHABET)) != 26:
		raise ValueError("Cheia trebuie sa fie o substitutie bijectiva a alfabetului.")

	print("Frecventele literelor cifrate:")
	for letter, count, percentage in letter_frequencies(CIPHERTEXT):
		print(f"{letter}: {count:4} aparitii ({percentage:5.2f}%)")

	print("\nMesajul descifrat:\n")
	plaintext = decrypt(CIPHERTEXT).replace("\u2014", "-")
	print(plaintext)


if __name__ == "__main__":
	main()
