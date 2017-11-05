//
//  ViewController.m
//  Who Dares Cares
//
//  Created by Gabor Daniel Borics-Kurti on 05/11/2017.
//  Copyright © 2017 codeforfood. All rights reserved.
//

#import "ViewController.h"

@implementation ViewController

-(void)viewDidLoad {
    [super viewDidLoad];
    
    NSString *mainPage = @"http://127.0.0.1:8000/";
    
    WKWebViewConfiguration *config = [[WKWebViewConfiguration alloc] init];
    WKWebView *webView = [[WKWebView alloc] initWithFrame:self.outerView.frame configuration:config];
    webView.navigationDelegate = self;
    NSURLRequest *nsrequest=[NSURLRequest requestWithURL:[NSURL URLWithString:mainPage]];
    [webView loadRequest:nsrequest];
    [self.outerView addSubview:webView];
}

@end
