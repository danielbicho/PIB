function createCaptcha()

for j=1:10
    captcha = [];
    for i=1:4
        c = getChar();
        safe_color = getRandomSafeColors();
        H = vision.TextInserter(c);
        H.Color = safe_color;
        H.FontSize = 60;
        H.Font = getFamily();
        I = ones(75,45,3);
        v=0.1;
        IN = imnoise(I(:,:,:),'speckle',v);
        InsertedImage = step(H, IN);
        captcha = [captcha InsertedImage];
    end
    imwrite( captcha, strcat('captcha',int2str(j),'.png') );
end

function f = getFamily()

fonts={'Algerian',
    'Arial',
    'Arial Black',
    'Arial Narrow',
    'Arial Unicode MS',
    'Book Antiqua',
    'Bookman Old Style'};

lfSize = size(fonts,1);
randFF = randi([1,lfSize],1);
ff = cellstr(fonts);
faux = ff(randFF);
f = faux{1}

function c = getChar()

randSet = randi([1,3],1);
switch randSet
  case 1
      c = char(randi([48,57],1));
  case 2
      c = char(randi([65,90],1));
  case 3
      c = char(randi([97,122],1));
    otherwise
      c = char(32);
end


