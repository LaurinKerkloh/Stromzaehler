const interval = 10000;
const topic = "tele/Solar/SENSOR";

Timer.set(interval, true, function () {
  // Get EM data
  let em = Shelly.getComponentStatus("em", 0);
  let emData = Shelly.getComponentStatus("emdata", 0);

  let totalPower = em.total_act_power; // Total active power (W)
  let totalEnergy = emData.total_act; // Total energy consumed (Wh)

  // Create JSON payload
  let payload = JSON.stringify({
    Time: new Date().toISOString(),
    Solar: {
      reading: totalEnergy,
      current_power: totalPower,
    },
  });

  // Publish to MQTT
  MQTT.publish(topic, payload, 0, false);
});
