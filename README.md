# OAI Data Viewer
## John's Ideas for Improvement
### General
- It could be good to let users add in data... This could cause problems, but it also could make this program more flexible. I'm mostly thinking of this as the data this was started with was incomplete. (missing some time points, some things just not transferred to UCAIR yet...)
- Add units to axes
- Add to legend (including for average line, clarifying that it is the average across cases at time point)
    - Is average across all total cases or all filtered cases?
- Instead of removing checkboxes for non-existant timepoints, perhaps gray it out??
    - This may not be an improvement, but could be worth exploring. I think the removal may make it slightly confusing to see what is going on. Also, graying it out would make it more obvious to the user that the timepoint doesn't exist, which could be helpful in discovering missing data (hopefully this would never happen).
        - ***I found some patients where some expected time points seeem to be missing, so we probably do want to implement this change***
            - e.g. The top two results for "Diabetes" have discrepencies on the right side. Patient 9003316 has [0, 12, 24, 36, 48, 96], but Patient 9003406 has [0, 12, 24, 30, 36, 48, 72, 96].
        - Additionally, 
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
    - Implementation idea:
        - Filter out points that are outside of threshold, then add them separately with an edge color (edge coloration as seen [here](https://matplotlib.org/stable/users/explain/quick_start.html#colors))
- Let user filter cases with certain confidence threshold variation
- Keep range the same across patients for an easier comparison
    - This will also keep the gray line in the same position
    - Let the user set the range, or zoom in/out as necessary
- Lines 54-55 (before branch)
    ```
    root.grid_rowconfigure(2, weight=1) # make the canvas expand to fill the entire grid
    root.grid_columnconfigure(0, weight=1) # make the canvas expand to fill the entire grid
    ```
    - Look into this. Xiangjian said that changing values had no impact
- Line 252 - 258 (current branch)
    ```
    # Calculate and plot the average value for all data at the current time point and side
    # Here is little redundant, but it is easy to implement
    all_data = data_loc[(data_loc['tp'] == int(0)) & (data_loc['side'] == side)]
    average_value = all_data.groupby('loc')[which_measure].mean()

    avg_values_to_plot = average_value.reindex(sorted_data['loc'])
    ax.plot(sorted_data['loc'], avg_values_to_plot, linestyle='--', color='grey')
    ```
    - Xiangjian says there is a potential for performance improvements (John, look into this)
    - Relevant comment from John:
    > It would be better to move the average calculation out of the loop. For some reason it relies on the filtered_data in the loop though...

### Completed improvements
- Improved padding and spacing of checkboxes and radiobuttons
- Moved "Patient Information" button to avoid overlap with checkboxes when window is too small
- Created a minsize for the window
- Let user quickly view the number of cases
- Moved all selections to the top right
- Created labels for all selection fields