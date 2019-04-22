# import rcpy libraries
import rcpy
import rcpy.adc as adc

# Read ADC channels via function calls.
for ch in range(adc.CHANNEL_COUNT):
    raw = adc.get_raw(ch)
    voltage = adc.get_voltage(ch)
    print("channel={} : raw={:4} voltage={:+6.2f}".format(ch, raw, voltage))

