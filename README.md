# OAI Data Viewer
## John's Ideas for Improvement
### General
- Add units to axes
- Add to legend (including for average line, clarifying that it is the average across cases at time point)
    - Is average across all total cases or all filtered cases?
- Instead of removing checkboxes for non-existant timepoints, perhaps gray it out??
    - This may not be an improvement, but could be worth exploring. I think the removal may make it slightly confusing to see what is going on. Also, graying it out would make it more obvious to the user that the timepoint doesn't exist, which could be helpful in discovering missing data (hopefully this would never happen).
- Colors--do we need to consider colorblindness? (low priority, I'm not aware of anyone in the lab having this accessibliy need)
    - Check how current color scheme does for various color blindness types with [Coblis](https://www.color-blindness.com/coblis-color-blindness-simulator/)
- Optimize line thickness to be able to view different lines comparatively
- Dots are a bit large, which can make it difficult to see dots from the same tp for different lines
- Does this framework support hover effects?
    - Potential uses:
        - Get exact value when hover over point
        - Vertical bar that shows values for each selected 
- It could be good to add a search/autocomplete function to the patient id combobox
    - Some possible solutions found here:
        - https://www.tutorialspoint.com/how-to-create-a-combo-box-with-auto-completion-in-tkinter
        - https://www.geeksforgeeks.org/autocmplete-combobox-in-python-tkinter/
        - https://codereview.stackexchange.com/questions/112104/searching-combobox-drop-down-list
- What does the "Risk" filter mean?
### Slice viewer
- Let user set a threshold and color points that are outside of that threshold
- Let user filter cases with certain confidence threshold variation
- Keep range the same across patients for an easier comparison
    - This will also keep the gray line in the same position
    - Let the user set the range, or zoom in/out as necessary
- Lines 54-55
    - Look into this. Xiangjian said that changing values had no impact
- Lines 172-176
    - Potential for performance improvements?

### Completed improvements
- Improved padding and spacing of checkboxes and radiobuttons
- Moved "Patient Information" button to avoid overlap with checkboxes when window is too small
- Created a minsize for the window
- Let user quickly view the number of cases
- Moved all selections to the top right
- Created labels for all selection fields