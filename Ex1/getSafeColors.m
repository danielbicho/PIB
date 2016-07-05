function safe_colors = getSafeColors()

safe_values = 0 : 51 : 255;
safe_colors = [];
for r = safe_values
    for g = safe_values
        for b = safe_values
            safe_colors = [safe_colors; [r g b]];
        end
    end
end
