### F. Coin ledger (mean k coins per farm; costs negative). Raw means and shop-matched differences
Shop-matched: for every farm of ours, the mean of its 3 nearest TOP1-5 farms by shop-demand vector (units the town consumes of each product over the game, z-scored); diff = matched top - ours, se over our farms.
| line | TOP1-5 raw | TOP1-3 raw | V183 | v183ms | lx3 | top5 - V183+ms raw | top5(matched) - V183+ms (se) | top3(matched) - V183+ms (se) |
|---|---|---|---|---|---|---|---|---|
| rev_STRAWBERRY | +34.1 | +33.7 | +35.8 | +20.7 | +33.5 | +3.1 | +4.9 (1.7) | +4.3 (2.0) |
| rev_MILK | +21.2 | +22.2 | +22.5 | +20.9 | +23.1 | -0.8 | -1.8 (1.5) | -1.5 (1.7) |
| rev_WOOL | +18.1 | +18.9 | +14.3 | +17.5 | +16.7 | +2.8 | +0.5 (1.6) | +0.2 (1.5) |
| rev_MELON | +14.4 | +14.3 | +13.8 | +13.7 | +13.4 | +0.7 | +0.8 (0.2) | +0.7 (0.2) |
| rev_TOMATO | +7.9 | +8.8 | +2.3 | +2.6 | +0.0 | +5.5 | +5.2 (1.0) | +7.2 (1.0) |
| rev_EGG | +10.6 | +10.1 | +12.2 | +13.0 | +11.9 | -1.9 | -1.3 (0.7) | -1.8 (0.7) |
| rev_CARROT | +5.7 | +5.8 | +5.6 | +8.1 | +6.9 | -0.7 | -0.2 (0.8) | +0.1 (0.8) |
| rev_WHEAT | +16.9 | +17.8 | +40.8 | +48.5 | +39.2 | -26.3 | -26.7 (1.3) | -25.1 (1.3) |
| rev_FERT | +12.4 | +12.3 | +19.4 | +21.9 | +19.7 | -7.8 | -7.7 (0.4) | -7.9 (0.4) |
| buy_WHEAT | -4.9 | -4.9 | -32.0 | -38.4 | -31.3 | +29.1 | +29.1 (1.3) | +29.1 (1.3) |
| buy_FERT | -0.0 | -0.0 | -6.7 | -9.1 | -6.6 | +7.4 | +7.4 (0.4) | +7.4 (0.4) |
| seed_WHEAT | -1.8 | -1.9 | -1.6 | -1.7 | -1.6 | -0.2 | -0.1 (0.0) | -0.3 (0.1) |
| seed_CARROT | -0.9 | -0.9 | -0.7 | -1.0 | -0.9 | -0.1 | -0.2 (0.1) | -0.2 (0.1) |
| seed_TOMATO | -0.8 | -1.0 | -0.1 | -0.1 | +0.0 | -0.8 | -0.7 (0.0) | -1.0 (0.0) |
| seed_STRAWBERRY | -3.3 | -3.3 | -3.5 | -2.8 | -3.2 | +0.0 | -0.1 (0.1) | -0.0 (0.1) |
| seed_MELON | -1.0 | -1.0 | -0.9 | -1.0 | -0.9 | -0.0 | -0.0 (0.0) | -0.0 (0.0) |
| animal_GOOSE | -2.2 | -2.2 | -2.1 | -2.2 | -2.1 | -0.0 | -0.1 (0.1) | -0.1 (0.1) |
| animal_COW | -3.4 | -3.5 | -3.3 | -3.1 | -3.0 | -0.2 | -0.2 (0.1) | -0.3 (0.1) |
| animal_SHEEP | -3.3 | -3.6 | -2.8 | -3.0 | -3.5 | -0.5 | -0.1 (0.2) | -0.2 (0.2) |
| hires | -7.0 | -7.7 | -5.3 | -5.5 | -5.6 | -1.6 | -1.5 (0.2) | -2.4 (0.1) |
| land | -5.9 | -7.0 | -3.0 | -3.0 | -3.0 | -2.9 | -2.8 (0.2) | -4.0 (0.0) |
| final | +109.8 | +110.1 | +108.0 | +98.9 | +105.7 | +4.7 | +4.4 (2.6) | +4.1 (2.7) |

Matched-pair mean shop-demand distance: 1.49 (nearest), typical random pair 3.46

### G. Net lines (revenue minus own input costs), k coins, shop-matched TOP1-5 minus V183+v183ms
| net line | top5 matched - ours (se) | top3 matched - ours (se) | TOP1-5 raw | V183+ms raw |
|---|---|---|---|---|
| wheat (rev - wheat buys - wheat seed) | +2.3 (0.5) | +3.8 (0.6) | +10.2 | +7.6 |
| strawberry (rev - seed) | +4.8 (1.7) | +4.2 (1.9) | +30.8 | +27.7 |
| tomato (rev - seed) | +4.5 (0.9) | +6.2 (0.9) | +7.1 | +2.3 |
| melon (rev - seed) | +0.8 (0.2) | +0.6 (0.2) | +13.5 | +12.8 |
| carrot (rev - seed) | -0.3 (0.7) | -0.2 (0.8) | +4.8 | +5.6 |
| milk (rev - cows) | -2.0 (1.4) | -1.8 (1.6) | +17.8 | +18.8 |
| wool (rev - sheep) | +0.4 (1.4) | +0.0 (1.3) | +14.8 | +12.5 |
| egg (rev - geese) | -1.4 (0.6) | -1.9 (0.5) | +8.4 | +10.3 |
| hires | -1.5 (0.2) | -2.4 (0.1) | -7.0 | -5.4 |
| land | -2.8 (0.2) | -4.0 (0.0) | -5.9 | -3.0 |
| fertiliser (buys + sales) | -0.3 (0.2) | -0.5 (0.2) | +12.4 | +12.8 |
| FINAL | +4.4 (2.6) | +4.1 (2.7) | +109.8 | +105.1 |