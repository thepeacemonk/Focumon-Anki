import re
import unittest

# HTML Snippets provided by user
HTML_STATS = """
<div class="flex flex-col bg-retro-base-150 dark:bg-base-200 p-2 pb-4 rounded text-sm">
        <p class="text-xl opacity-50 mb-2">My Stats</p>

        <div class="flex justify-between tooltip px-1 mb-0.5 font-sans tracking-tighter" data-tip="Each Trainer Level boosts Focumon EXP by 0.1%">
          <p class="font-serif">Focumon EXP Boost</p>
          <p class="opacity-50 font-serif">+3.6%</p>
        </div>

        <div onclick="loot_limit_modal.showModal()" class="px-1 hover:cursor-pointer hover:bg-base-300 transition duration-200 rounded">
          <progress class="progress  w-full" value="0" max="100"></progress>
          <div class="flex justify-between -mt-1 tracking-tighter">
            <p>Loot Collection</p>
            <p class="opacity-50">
                0/6
            </p>
          </div>
        </div>
        
        <div id="stamina_and_recovery_widget" class="text-sm font-serif">
  <div onclick="stamina_recovery_modal.showModal()" class="px-1 hover:cursor-pointer hover:bg-base-300 transition duration-200 rounded">
    <progress class="progress progress-success w-full" value="100" max="100"></progress>
    <div class="flex justify-between -mt-1 tracking-tighter">
      <p>Trainer Stamina</p>
      <p class="opacity-50">85/85</p>
    </div>
  </div>
</div>

          <div class="px-1 tooltip font-sans tracking-tighter" data-tip="Focus in training centers to earn Trainer EXP">
            <progress class="progress progress-accent w-full" value="75" max="100"></progress>
            <div class="flex justify-between -mt-1 mb-3 font-serif">
              <p>Trainer EXP</p>
              <p class="opacity-50">273/360</p>
            </div>
          </div>
"""

HTML_LEVEL = """
<div class="relative hidden md:flex w-full max-w-lg mt-4 md:mt-0 flex-col items-start">
<!-- ... -->
      <div class="relative font-serif w-full pt-4">
  <div class="flex gap-x-2 justify-center items-end mb-2 font-sans font-bold">
    <div class="z-20 flex-shrink-0 pt-1 tooltip" data-tip="@PeaceMonk">
      <img class="h-32 w-32 flex-shrink-0 select-none pointer-events-none" style="image-rendering: pixelated;" src="/assets/trainer/battle/059-d662f48e.png">
    </div>
      <div class="z-10 flex-shrink-0 -ml-14 pb-1 tooltip" data-tip="Hemling">
        <div class="h-32 w-32 relative overflow-hidden flex-shrink-0 select-none pointer-events-none animate-jumping-bounce-always" style="image-rendering: pixelated;"><img class="h-32 w-32" src="/assets/focumon/battle/098-b0350d43.png"></div>
      </div>
  </div>
  <div class="flex gap-x-4 justify-center items-end mb-4">
    <div class="badge dark:border-base-content dark:border-opacity-50">LV.36</div>
      <div class="badge dark:border-base-content dark:border-opacity-50">LV.17</div>
  </div>
<!-- ... -->
</div>
"""

def extract_stats(html_content):
    stats = {}
    
    # Loot Collection
    # Search for Loot Collection text, then find the next p tag with opacity-50
    # Or just regex the structure loosely
    loot_match = re.search(r'Loot Collection</p>\s*<p[^>]*>\s*([\d/]+)\s*</p>', html_content, re.DOTALL)
    if loot_match:
        stats['loot_collection'] = loot_match.group(1).strip()
        
    # Stamina
    stamina_match = re.search(r'Trainer Stamina</p>\s*<p[^>]*>\s*([\d/]+)\s*</p>', html_content, re.DOTALL)
    if stamina_match:
        stats['stamina'] = stamina_match.group(1).strip()

    # Trainer EXP
    exp_match = re.search(r'Trainer EXP</p>\s*<p[^>]*>\s*([\d/]+)\s*</p>', html_content, re.DOTALL)
    if exp_match:
        stats['trainer_exp'] = exp_match.group(1).strip()

    return stats

def extract_focumon_level(html_content):
    # Find all badges with LV.
    badges = re.findall(r'<div class="badge[^>]*">LV\.(\d+)</div>', html_content)
    if len(badges) >= 2:
        # Assuming second badge is Focumon level based on user description
        return badges[1]
    return None

class TestParsing(unittest.TestCase):
    def test_stats(self):
        stats = extract_stats(HTML_STATS)
        self.assertEqual(stats.get('loot_collection'), '0/6')
        self.assertEqual(stats.get('stamina'), '85/85')
        self.assertEqual(stats.get('trainer_exp'), '273/360')

    def test_level(self):
        level = extract_focumon_level(HTML_LEVEL)
        self.assertEqual(level, '17')

if __name__ == '__main__':
    unittest.main()
