//
//  ViewController.m
//  Sidekick
//
//  Created by Spencer Kaiser on 8/31/15.
//  Copyright (c) 2015 Sidekick Predictive Technologies. All rights reserved.
//

#import "ViewController.h"

@interface ViewController ()

@property (weak, nonatomic) IBOutlet UITextField *nameTextField;
@property (weak, nonatomic) IBOutlet UITextField *phoneNumberTextField;

@end

@implementation ViewController

- (void)viewDidLoad {
    [super viewDidLoad];
    // Do any additional setup after loading the view, typically from a nib.
    
    self.nameTextField.delegate = self;
    [self.nameTextField addTarget:self
                           action:@selector(nameFieldChanged:)
                 forControlEvents:UIControlEventEditingChanged];
    
    self.phoneNumberTextField.delegate = self;
    [self.phoneNumberTextField addTarget:self
                                  action:@selector(phoneNumberFieldChanged:)
                        forControlEvents:UIControlEventEditingChanged];
    
    //Auto capitalize words in name field
    self.nameTextField.autocapitalizationType = UITextAutocapitalizationTypeWords;
    
}

- (void)didReceiveMemoryWarning {
    [super didReceiveMemoryWarning];
    // Dispose of any resources that can be recreated.
}

#pragma mark -
#pragma mark User Info View

- (BOOL)textFieldShouldReturn:(UITextField *)textField {
    if (textField == self.nameTextField) {
        [self.phoneNumberTextField becomeFirstResponder];
    }
    return YES;
}


- (void)touchesBegan:(NSSet *)touches withEvent:(UIEvent *)event {
    [self closeKeyboard];
}

-(void)closeKeyboard{
    [self.view endEditing:YES];
}

-(void)nameFieldChanged:(UITextField *)nameTextField
{
    NSLog(@"text changed: %@", nameTextField.text);
    
    //    NSString *textFieldText = [nameTextField.text stringByReplacingOccurrencesOfString:@"," withString:@""];
    //
    //    NSNumberFormatter *formatter = [[NSNumberFormatter alloc] init];
    //    [formatter setNumberStyle:NSNumberFormatterDecimalStyle];
    //    NSString *formattedOutput = [formatter stringFromNumber:[NSNumber numberWithInt:[textFieldText integerValue]]];
    //    nameTextField.text=formattedOutput;
}

-(void)phoneNumberFieldChanged:(UITextField *)phoneNumberTextField
{
    //Get a clean copy of the phone number without formatting characters
    NSCharacterSet *formattingChars = [NSCharacterSet characterSetWithCharactersInString:@"() -;,+*"];
    NSString *strippedPhoneNumber = [[phoneNumberTextField.text componentsSeparatedByCharactersInSet: formattingChars] componentsJoinedByString: @""];
    
    NSLog(@"Cleaned Number: %@", strippedPhoneNumber);
    
    NSString *formattedPhoneNumber;
    
    
    if (strippedPhoneNumber.length <= 3){
        formattedPhoneNumber = [NSString stringWithFormat:@"(%@)", strippedPhoneNumber];
    } else if (strippedPhoneNumber.length <= 10){
        NSString *areaCode = [strippedPhoneNumber substringToIndex:3];
        NSString *firstThree = @"", *lastFour = @"";
        if (strippedPhoneNumber.length <= 6){
            firstThree = [strippedPhoneNumber substringWithRange:NSMakeRange(3, strippedPhoneNumber.length - 3)];
        } else {
            firstThree = [strippedPhoneNumber substringWithRange:NSMakeRange(3, 3)];
            lastFour = [strippedPhoneNumber substringFromIndex:6];
        }
        
        formattedPhoneNumber = [NSString stringWithFormat:@"(%@) %@", areaCode, firstThree];
        if (lastFour.length > 0){
            formattedPhoneNumber = [NSString stringWithFormat:@"%@-%@", formattedPhoneNumber, lastFour];
        }
    }
    
    phoneNumberTextField.text = formattedPhoneNumber;
    
    //If the user has changed the phone number text and the new value is 10 digits (complete number), close keyboard
    if(strippedPhoneNumber.length >= 10){
        [self closeKeyboard];
    }
}

@end
