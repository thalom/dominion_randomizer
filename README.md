# dominion_randomizer

## It's a Command Line Tool!

### Use

Open up your terminal and run <pre><code>python shuffler.py</code></pre> for a totally random board.<br>
The following options are available:<br>
<code>-a</code> for any attacks<br>
<code>-w</code> for turn-worsening attacks<br>
<code>-r</code> for trashing attacks<br>
<code>-p</code> for topdeck attacks<br>
<code>-h</code> for handsize attacks<br>
<code>-i</code> for deck-inspection attacks<br>
<code>-c</code> for junking attacks<br>
<code>-b</code> for +buy<br>
<code>-d</code> for +cards<br>
<code>-g</code> for gainers<br>
<code>-s</code> for sifters<br>
<code>-t</code> for trashers<br>
<code>-v</code> for villages<br>
<code>-u</code> for durations<br>
<code>-n</code> for cantrips<br>
<code>-T</code> for alternative treasures<br>
<code>-V</code> for alternative victory cards<br>
<code>-L</code> for the probability of including a landscape<br>
<code>-C</code> for the probability of including colonies and platina<br>
<code>-S</code> for the probability of including shelters<br>
<code>-e</code> for specifying which expansions to include<br>
<p><ul><li>-L, -C, and -S take a value between 0 and 1 to specify their respective inclusion probability. <li>Any of the other options may be paired with 'y' or 'i' to require the inclusion of one card from that category; <li>'n' or 'x' to exclude any cards of that category; an integer from 2-9 to require the inclusion of that many cards of that category; <li>an integer and 's' (e.g. '1s') to require that many <i>strong</i> cards of that category <ul><li>instead of 's', you may use 'r' for remodelers with the trashing option; <li>instead of 's', you may use 't' for throne room variants with the village option; <li>attacks actually refers to any interpersonal interactions, but refers to attacks with 's'; <li>junkers actually includes secondary cursers, but refers strictly to primary junkers with 's'; <li>draw actually has four degrees ranging between 'v', 's', 'm', 'w' (very strong, strong, medium, weak; each weaker category also includes all the cards of all stronger categories); <li>treasures, durations, cantrips, and specific attack types other than junkers do not have <i>strong</i> versions of those categories.</ul></ul></p>

### Examples

<pre><code>python shuffler.py -h x -c x -d 1v -v y -b y</code></pre>
The above line would give you a board without handsize attacks, without junking attacks, with at least one non-terminal draw, with at least one village, with at least one buy.
<pre><code>python shuffler.py -L 0.75 -S 0.333 -C 0.85 -e base adventures renaissance prosperity dark_ages</code></pre>
The above line would give you a board with a 75% chance to include each of two landscapes, a 33.3% chance to include shelters, an 85% chance to include colonies and platina, and cards would only be selected from the Base, Adventures, Renaissance, Prosperity, and Dark Ages sets (oh yeah, you have to write 'dark_ages').
<p>The output will also be saved into a file "output.txt" that you can easily copy/paste into <a href=https://dominion.games>dominion.games</a> </p>

### Features not yet implemented

<p><ul><li>An option to specify costs of cards<li>Within the expansions option, a way to specify which expansions to exclude rather than include<li>Any options for specifying landscapes (other than the raw probability that one is included)</ul>
</p>
