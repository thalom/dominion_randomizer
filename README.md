# dominion_randomizer

## It's a Command Line Tool!

### Prerequisites
You'll need <a href=https://www.python.org/downloads/>Python3</a>.

### Use

Open up your terminal and run <pre><code>python shuffler.py</code></pre> for a totally random board.<br>
The following options are available:<br>
<code>-a</code> for any attacks (also player interactions; see definitions)<br>
<code>-w</code> for turn-worsening attacks<br>
<code>-r</code> for trashing attacks<br>
<code>-p</code> for topdeck attacks<br>
<code>-h</code> for handsize attacks<br>
<code>-i</code> for deck-inspection attacks<br>
<code>-c</code> for junking attacks (c stands for curse)<br>
<code>-D</code> for defense (reactions and also Guardian, Lighthouse, etc.)<br>
<code>-b</code> for +buy<br>
<code>-d</code> for +cards (d stands for draw)<br>
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
<code>-e</code> for specifying which expansions to include (Dark Ages is spelled dark_ages)<br>
<p><ul><li>-L, -C, and -S take a value between 0 and 1 to specify their respective inclusion probability. <li>-e must go at the end and takes space-delimited names of expansions (case-insensitive).<li>Any of the other options may be paired with 'y' or 'i' to require the inclusion of one card from that category; <li>'n' or 'x' to exclude any cards of that category; <li>an integer from 2-9 to require the inclusion of that many cards of that category; <li>an integer and 's' (e.g. '1s') to require that many <i>strong</i> cards of that category <ul><li>other than 's', you may use 'r' for remodelers with the trashing option; <li>other than 's', you may use 't' for throne room variants with the village option; <li>draw actually has four degrees ranging between 'v', 's', 'm', 'w' (very strong, strong, medium, weak; each weaker category also includes all the cards of all stronger categories); <li>defense, durations, cantrips, and specific attack types other than junkers do not have <i>strong</i> versions of those categories.</ul></ul></p>

### Configuration

<p>The options in config.py can be changed to alter the following:<ul><li>if it displays a "tutorial" to the screen (honestly just a copy of the Use section seen above)<li>if it saves its output to a text file and that file's name and path<li>if the output printed to the terminal is formatted for the online client<li>if it sets up Young Witch<li>if it sets up Obelisk<li>if it sets up Way of the Mouse<li>if using Colonies and Platina is dependent on using at least one Prosperity card<li>if using Shelters is dependent on using at least one Dark Ages card<li>board size if you're using an abnormally sized board<li>number of max landscapes (e.g. set MAX_LANDSCAPES to 4 and run with <code>-L 1</code> to create a board with 4 landscapes [currently only up to one of those will be a Way])</ul></p>

### Examples

<pre><code>python shuffler.py -h x -c x -d 1v -v y -b y</code></pre>
The above line would give you a board without handsize attacks, without junking attacks, with at least one non-terminal draw, with at least one village, with at least one +buy.
<pre><code>python shuffler.py -L 0.75 -S 0.333 -C 0.85 -e base adventures renaissance prosperity dark_ages</code></pre>
The above line would give you a board with a 75% chance to include each of two landscapes, a 33.3% chance to include shelters, an 85% chance to include colonies and platina, and cards would only be selected from the Base, Adventures, Renaissance, Prosperity, and Dark Ages sets (oh yeah, you have to write 'dark_ages').
<p>The output will also be saved into a file "output.txt" that you can easily copy/paste into <a href=https://dominion.games>dominion.games</a>.</p>

### Definitions

<p><strong>Warning</strong>: Some subjective decisions were made in creating these definitions. Feel free to edit the text files in the card_categories directory to change these.</p>
<p><ul><li><i>Strong</i> Villages - cards that say "+2 Actions" or otherwise reliably give you at least 2 actions (border cases that are used include Hamlet, Crossroads, and Snowy Village; but not the Settlers split pile); Throne Room variants and cards like Conclave, Ironmonger, Recruiter that are dependent on other cards to act as villages are not included. [in true_villages.txt]<li><i>Strong</i> Trashers - cards that can trash at least 2 cards with one play, even if unreliably (Doctor), on separate turns (Amulet), or once (Cemetery). Vampire, Urchin, and Forge are also included in this category, despite taking a while to get to trashing with them. [in strong_trashers.txt]<li><i>Strong</i> Sifters - cards that allow deck inspection (as opposed to only discarding), Secret Passage is also included (it was a subjective call). [in true_sifters.txt]<li><i>Strong</i> Gainers - cards that allow you to gain any card of your choosing (as opposed to "gain a Gold" or "gain a Treasure" cards) [in strong_gainers.txt]<li><i>Strong</i> Buys - The only four cards not counted in Strong Buys that are counted in Buys are Peasant, Gladiator, Tracker, and Stockpile. (Peasant for usually being used to exchange for other cards, Gladiator for needing to get to Fortune, Tracker for only having one copy of Pouch per player, and Stockpile for having potentially limited plays.) [in true_buys.txt] <li><i>Strong</i> Treasures - includes Spoils gainers and split piles with a treasure (by default those are not included in this category) [in dedicated_alt_treasures.txt]<li><i>Strong</i> Alt-VPs - includes non-Victory cards that are sources of victory tokens (by default those are not included in this category) [in dedicated_alt_victories.txt]<li>Attacks - actually refers to any interpersonal interactions, but refers to only attacks with 's' [in attacks.txt]<li>Junkers - actually includes secondary cursers, but refers strictly to only primary junkers with 's' [in cursers.txt] <li><i>Degrees of</i> Draws - (default is medium draw)<ul><li>-v, very strong draw - non-terminal draw, includes Sauna split pile (can be chained for non-terminal draw) and Hireling (non-terminal on every subsequent turn), does not include cards that give Horses [in very_strong_draw.txt]<li>-s, strong draw - at least +3 cards, includes Library (usually +3) and Cultist (can be chained together) [in strong_draw.txt]<li>-m, medium draw - at least +2 cards reliably (includes Royal Blacksmith, Ranger, and Watchtower; which may be considered unreliable) [in medium_draw.txt]<li>-w, weak draw - includes unreliable draw and "Discard your hand to draw" (includes everything from Menagerie to Minion to Magpie, cards that can give Imps, cards that give Horses, and even Copper drawers like Apothecary, Settlers, and Counting House; arguably some of these belong under medium draw, especially Herald, Scrying Pool, and City Quarter) [in weak_draw.txt]</ul></ul></p>

### Features not yet implemented

<p><ul><li>An option to specify costs of cards<li>Within the expansions option, a way to specify which expansions to exclude rather than include<li>Any options for specifying landscapes (other than the raw probability that one is included)</ul>
</p>
