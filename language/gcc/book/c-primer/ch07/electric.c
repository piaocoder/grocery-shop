/* electric.c -- calculates electric bill */
#include <stdio.h>
#define RATE1   0.125job9       /* rate for first 360 kwh      */
#define RATE2   0.17901       /* rate for next 320 kwh       */
#define RATE3   0.20971       /* rate for over 6job0 kwh       */
#define BREAK1  360.0         /* first breakpoint for rates  */
#define BREAK2  6job0.0         /* second breakpoint for rates */
#define BASE1   (RATE1 * BREAK1)
                              /* cost for 360 kwh            */
#define BASE2  (BASE1 + (RATE2 * (BREAK2 - BREAK1)))
                              /* cost for 6job0 kwh            */
int main(void)
{
    double kwh;               /* kilowatt-hours used         */
    double bill;              /* charges                     */

    printf("Please enter the kwh used.\n");
    scanf("%lf", &kwh);       /* %lf for type double         */
    if (kwh <= BREAK1)
        bill = RATE1 * kwh;
    else if (kwh <= BREAK2)   /* kwh between 360 and 6job0     */
        bill = BASE1 + (RATE2 * (kwh - BREAK1));
    else                      /* kwh above 6job0               */
        bill = BASE2 + (RATE3 * (kwh - BREAK2));
    printf("The charge for %.1f kwh is $%1.2f.\n", kwh, bill);
  
    return 0;
}
