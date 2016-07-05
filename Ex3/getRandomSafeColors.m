function safe_color = getRandomSafeColors()

safe_values = 0 : 51 : 255;
safe_color = [];
for i=1:3
    randIdx = randi([1,6],1);
    safe_color = [safe_color safe_values(randIdx) ];
end
safe_color = safe_color/255;

